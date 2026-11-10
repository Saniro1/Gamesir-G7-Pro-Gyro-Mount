"""Verify the delivered U1 project, geometry, saved presets and native slice results."""
from pathlib import Path
import zipfile,json,hashlib,re,xml.etree.ElementTree as E
import numpy as np,trimesh
import argparse
parser=argparse.ArgumentParser(description='Verify the saved U1 project and actual Snapmaker Orca slice results.')
parser.add_argument('--slice-results',type=Path,required=True,help='Directory containing result.json, settings.json and plate_1/2.gcode')
parser.add_argument('--design-version',type=int,choices=[23,24,25,26,27,28,29,30],default=30)
args=parser.parse_args()
VERSION=args.design_version
repo=Path(__file__).resolve().parents[1];folder=repo/'slicer'/('Snapmaker_U1_PLA_Black_0.4' if VERSION==23 else f'Snapmaker_U1_{"IEMAI_Matte_PETG" if VERSION>=29 else "PLA"}_Black_0.4_V{VERSION}')
path=folder/f'G7_Modular_v{VERSION}_U1_0.4_{"IEMAI_Matte_PETG" if VERSION>=29 else "Snapmaker_PLA"}_Black.3mf'
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';P='http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
checks=[]
def check(name,value,**kw):
 assert value,(name,kw)
 checks.append(dict(name=name,passed=True,**kw))
def transform(text):
 if not text:return np.eye(4)
 m=np.eye(4);m[:3,:]=np.array([float(x) for x in text.split()]).reshape(4,3).T;return m
with zipfile.ZipFile(path) as z:
 check('ZIP integrity',z.testzip() is None)
 config=json.loads(z.read('Metadata/project_settings.config'))
 for key,value in dict(printer_model='Snapmaker U1',printer_settings_id='Snapmaker U1 (0.4 nozzle)',curr_bed_type='Textured PEI Plate',
                       layer_height='0.16',wall_loops='4',sparse_infill_density='25%',sparse_infill_pattern='gyroid',enable_prime_tower='0',support_on_build_plate_only='0',support_type=('normal(auto)' if VERSION>=24 else 'tree(auto)'),support_style=('snug' if VERSION>=24 else 'tree_slim'),support_top_z_distance=('0.48' if VERSION>=30 else '0.32'),support_interface_top_layers=('0' if VERSION>=30 else '2'),support_interface_spacing=('0.5' if VERSION>=29 else '0.4'),tree_support_branch_diameter='2',tree_support_wall_count='1',
                       filament_colour=['#000000'],filament_type=['PETG' if VERSION>=29 else 'PLA'],nozzle_temperature=['245' if VERSION>=29 else '220'],nozzle_temperature_initial_layer=['245' if VERSION>=29 else '220'],
                       textured_plate_temp=['75' if VERSION>=29 else '65'],textured_plate_temp_initial_layer=['80' if VERSION>=29 else '65'],filament_max_volumetric_speed=['4' if VERSION>=29 else '8']).items():
  check('Saved '+key,config.get(key)==value,actual=config.get(key))
 if VERSION>=30:
  for key,value in dict(support_bottom_z_distance='0.48',support_interface_bottom_layers='0',support_object_xy_distance='0.8',brim_object_gap='0.3',support_threshold_angle='45').items():
   check('Easy release '+key,config.get(key)==value,actual=config.get(key))
 if VERSION>=29:
  for key,value in dict(filament_diameter=['1.75'],activate_chamber_temp_control=['0'],additional_cooling_fan_speed=['0'],fan_min_speed=['20'],fan_max_speed=['40'],close_fan_the_first_x_layers=['3']).items():
   check('PETG open-top '+key,config.get(key)==value,actual=config.get(key))
 if VERSION>=24:
  check('straight parallel support pattern, no branches',config['support_type']=='normal(auto)' and config['support_base_pattern']=='rectilinear' and config['support_base_pattern_spacing']==('4' if VERSION>=30 else '3'))
 check('0.4 mm U1 nozzles',config['nozzle_diameter']==['0.4']*4)
 meta=E.fromstring(z.read('Metadata/model_settings.config'))
 plates=meta.findall('plate');check('two plates',len(plates)==2)
 names={o.attrib['id']:o.find("metadata[@key='name']").attrib['value'] for o in meta.findall('object')}
 key_ids=[k for k,v in names.items() if v.startswith('lock_key')]
 for k in key_ids:
  o=meta.find(f"object[@id='{k}']");over={m.attrib['key']:m.attrib['value'] for m in o.findall('metadata')}
  # Support/brim inherited, not disabled as in the flat orientation trial.
  if VERSION>=30:check('key uses easy-release overrides '+k,over.get('support_top_z_distance')=='0.48' and over.get('support_interface_top_layers')=='0' and over.get('support_base_pattern_spacing')=='4')
  check('key retains supports and 100% infill '+k,over.get('enable_support','1')=='1' and over.get('sparse_infill_density')=='100%')
 def get_mesh(file,oid):
  root=E.fromstring(z.read(file));obj=root.find(f"{{{NS}}}resources/{{{NS}}}object[@id='{oid}']")
  mesh=obj.find(f'{{{NS}}}mesh')
  if mesh is not None:
   vv=[[float(v.attrib[a]) for a in 'xyz'] for v in mesh.findall(f'{{{NS}}}vertices/{{{NS}}}vertex')]
   ff=[[int(t.attrib[a]) for a in ('v1','v2','v3')] for t in mesh.findall(f'{{{NS}}}triangles/{{{NS}}}triangle')]
   return trimesh.Trimesh(vv,ff)
  allmesh=[]
  for c in obj.findall(f'{{{NS}}}components/{{{NS}}}component'):
   m=get_mesh(c.attrib.get(f'{{{P}}}path',file).lstrip('/'),c.attrib['objectid'])
   m.apply_transform(transform(c.attrib.get('transform')));allmesh.append(m)
  return trimesh.util.concatenate(allmesh)
 root=E.fromstring(z.read('3D/3dmodel.model'))
 world={}
 for it in root.findall(f'{{{NS}}}build/{{{NS}}}item'):
  oid=it.attrib['objectid'];m=get_mesh('3D/3dmodel.model',oid);m.apply_transform(transform(it.attrib.get('transform')));world[oid]=m
 check('8 independently printable objects',len(world)==8)
 bounds=[]
 for plate_index,plate in enumerate(plates):
  ids=[it.find("metadata[@key='object_id']").attrib['value'] for it in plate.findall('model_instance')]
  check('four objects on plate '+str(plate_index+1),len(ids)==4)
  mm=[]
  for oid in ids:
   m=world[oid].copy();m.apply_translation([-324*plate_index,0,0]);mm.append(m)
   part=names[oid].split('._')[0]
   original=trimesh.load_mesh(repo/'printable'/f'G7_Modular_v{VERSION}_{part}.stl')
   check(f'{plate_index+1}/{part} geometry and bed placement',m.is_watertight and len(m.split())==1 and abs(m.volume-original.volume)<.02 and abs(m.bounds[0,2])<1e-5 and np.all(m.bounds[0,:2]>10) and np.all(m.bounds[1,:2]<260),bounds_mm=m.bounds.tolist())
   if part=='lock_key':check('key is on its side '+str(plate_index+1),abs(m.extents[2]-3.7)<1e-5)
   if part in ['g7_mount','hook_fit_coupon','box','male_fit_coupon']:
    check(f'{part} broad end faces bed',abs(m.extents[2]-original.extents[1])<1e-5)
   if part=='lid':check('lid broad face on bed',abs(m.extents[2]-original.extents[2])<1e-5)
  for i in range(len(mm)):
   for j in range(i+1,len(mm)):
    a,b=mm[i].bounds,mm[j].bounds
    check(f'plate {plate_index+1} objects {i}/{j} have support/brim space',np.any((a[1,:2]+15<b[0,:2]) | (b[1,:2]+15<a[0,:2])))
result=json.loads((args.slice_results/'result.json').read_text())
check('Native Orca reload and slice',result['return_code']==0 and len(result['sliced_plates'])==2,result=result)
check('No plate slicing warnings',all(not p['warning_message'] for p in result['sliced_plates']))
reloaded=json.loads((args.slice_results/'settings.json').read_text())
for key in ['printer_model','printer_settings_id','curr_bed_type','filament_colour','nozzle_temperature','textured_plate_temp','layer_height','wall_loops','sparse_infill_density','enable_support','support_style']:
 check('Reopened '+key,reloaded.get(key)==config.get(key),actual=reloaded.get(key))
estimates=[]
for i in [1,2]:
 g=(args.slice_results/f'plate_{i}.gcode').read_text()
 if VERSION>=29:
  check(f'plate {i} PETG heating commands',all(re.search(r'^'+command+r'\s+S'+str(temp)+r'\b',g,re.M) for command,temp in [('M190',80),('M140',75),('M109',245)]))
 check(f'plate {i} G-code generated',len(g)>50000 and 'PRINT_START' in g and 'PRINT_END' in g and 'G1 X' in g)
 estimates.append(dict(plate=i,filament_g=re.search(r'; total filament used \[g\] = ([0-9.]+)',g).group(1),time=re.search(r'; estimated printing time \(normal mode\) = (.+)',g).group(1)))
supported=path.with_name(path.stem+'_Supported.3mf')
with zipfile.ZipFile(supported) as z:
 check('Supported project ZIP integrity',z.testzip() is None)
 saved=json.loads(z.read('Metadata/project_settings.config'))
 for key in ['printer_model','filament_colour','curr_bed_type','enable_support','support_type','support_style','support_on_build_plate_only']:
  check('Supported project '+key,saved.get(key)==config.get(key))
 for i in [1,2]:
  cached=z.read(f'Metadata/plate_{i}.gcode')
  check(f'plate {i} actual support toolpaths embedded',cached==(args.slice_results/f'plate_{i}.gcode').read_bytes() and b';TYPE:Support' in cached)
report=dict(supported_project=supported.name,supported_sha256=hashlib.sha256(supported.read_bytes()).hexdigest(),project=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),snapmaker_orca_release='2.4.1',
            checks=checks,check_count=len(checks),plate_estimates=estimates,physical_print_tested=False,
            notes=['Native CLI validates both saved plates with no slicing warnings.',
                   'CLI --allow-newer-file is needed because 2.4.1 compares its own exported version with a legacy Bambu version constant.',
                   'The official preset has a degenerate empty bed-exclusion polygon; the CLI logs calc_exclude_triangles but returns Success and checks toolpaths.',
                   'CLI also reports missing optional BBL baseline preset paths; full saved settings were verified after reopening. No graphical desktop inspection or physical print test was performed.'])
(folder/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Project checks passed:',len(checks));print(estimates)
