"""Build the two-plate U1 0.4 mm regular Snapmaker PLA Black project.

Uses manufacturer machine/material profiles bundled with Snapmaker Orca 2.4.1;
adds mechanical-part process settings without changing model geometry. Use the
existing checkout. See slicer/Snapmaker_U1_PLA_Black_0.4/README.md for details.
"""
from pathlib import Path
import json,shutil,sys,numpy as np,trimesh
import argparse,os,subprocess
parser=argparse.ArgumentParser(description='Create and optionally slice a U1 PLA Black project using Snapmaker Orca 2.4.1.')
parser.add_argument('--resources',type=Path,required=True,help='Snapmaker Orca resources directory')
parser.add_argument('--orca',required=True,help='Snapmaker Orca executable or runtime wrapper')
parser.add_argument('--workdir',type=Path,required=True,help='Writable scratch directory for oriented meshes and logs')
parser.add_argument('--validate',action='store_true',help='Reopen and slice both plates, retaining results in workdir')
args=parser.parse_args()
repo=Path(__file__).resolve().parents[1]
r=args.resources.resolve()/'profiles'/'Snapmaker'
o=repo/'slicer'/'Snapmaker_U1_PLA_Black_0.4'
w=args.workdir.resolve()
o.mkdir(parents=True,exist_ok=True)
(w/'models').mkdir(parents=True,exist_ok=True)
(w/'export').mkdir(exist_ok=True)
def profile(kind,name):
 d=json.loads((r/kind/(name+'.json')).read_text()); parent=d.get('inherits'); base=profile(kind,parent) if parent else {};base.update(d);return base
machine=profile('machine','Snapmaker U1 (0.4 nozzle)')
process=profile('process','0.16mm Standard @Snapmaker U1 (0.4 nozzle)')
filament=profile('filament','Snapmaker PLA Basic @U1')
for d in [machine,process,filament]:
 d['inherits']='';d['from']='User'
 for k in ['setting_id','renamed_from','description']:d.pop(k,None)
machine['printer_settings_id']=machine['name']
machine['from']='system'
process['inherits']='0.16mm Standard @Snapmaker U1 (0.4 nozzle)'
filament['inherits']='Snapmaker PLA Basic @U1'
process.update(name='G7 V23 - PLA fit and strength - 0.16mm @U1',print_settings_id='G7 V23 - PLA fit and strength - 0.16mm @U1',
 layer_height='0.16',initial_layer_print_height='0.20',wall_loops='4',top_shell_layers='6',bottom_shell_layers='5',
 sparse_infill_density='25%',sparse_infill_pattern='gyroid',wall_generator='arachne',
 outer_wall_speed=['40','40'],inner_wall_speed=['60','60'],sparse_infill_speed=['80','80'],internal_solid_infill_speed=['60','60'],top_surface_speed=['35','35'],gap_infill_speed='35',
 initial_layer_speed=['20','20'],initial_layer_infill_speed=['25','25'],bridge_speed=['20','20'],internal_bridge_speed=['25','25'],
 default_acceleration=['1500','1500'],outer_wall_acceleration=['1000','1000'],inner_wall_acceleration=['1500','1500'],travel_speed=['150','150'],
 enable_prime_tower='0',ooze_prevention='0',enable_support='1',support_type='normal(auto)',support_style='snug',support_threshold_angle='30',
 support_on_build_plate_only='1',support_top_z_distance='0.20',support_bottom_z_distance='0.20',support_interface_top_layers='3',support_object_xy_distance='0.35',
 support_speed=['50','50'],support_interface_speed=['30','30'],brim_type='outer_only',brim_width='5',brim_object_gap='0.15',
 curr_bed_type='Textured PEI Plate',print_sequence='by layer',elefant_foot_compensation='0.15',xy_hole_compensation='0',xy_contour_compensation='0')
filament['filament_max_volumetric_speed']=['8']
filament.update(name='Snapmaker PLA Basic Black @U1 - G7',filament_settings_id=['Snapmaker PLA Basic Black @U1 - G7'],default_filament_colour=['#000000'],filament_colour=['#000000'])
# CLI needs speed/acceleration vectors explicitly; the GUI normally migrates
# legacy scalar speed entries while reading system profiles.
for k in ['gap_infill_speed','overhang_totally_speed','initial_layer_acceleration','ironing_speed',
          'overhang_1_4_speed','overhang_2_4_speed','overhang_3_4_speed','overhang_4_4_speed',
          'top_surface_acceleration','slowdown_for_curled_perimeters']:
 if k in process and not isinstance(process[k],list):process[k]=[process[k],process[k]]
# Orca 2.4.1's partial-preset normalizer dereferences absent printer nozzles
# when this redundant default is present. Final combined config retains default 0.
process.pop('wipe_tower_filament',None)
for n,d in [('printer',machine),('process',process),('filament',filament)]:
 (o/(n+'.json')).write_text(json.dumps(d,indent=2)+'\n')
print('filament settings', {k:filament.get(k) for k in ['nozzle_temperature','nozzle_temperature_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer','filament_max_volumetric_speed','filament_type','filament_vendor']})
plates=[]
for name,parts in [('01 - Fit tests first',['hook_fit_coupon','universal_receiver','male_fit_coupon','lock_key']),('02 - Complete mount',['g7_mount','box','lid','lock_key'])]:
 objs=[]
 for part in parts:
  m=trimesh.load_mesh(repo/'printable'/f'G7_Modular_v23_{part}.stl')
  if part=='lock_key':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
  if part=='lid':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
  m.apply_translation([-m.bounds[0,0],-m.bounds[0,1],-m.bounds[0,2]])
  path=w/'models'/(part+'.stl');m.export(path)
  params={}
  if part in ['lid','universal_receiver']:
   params['enable_support']='0'
   params['brim_type']='no_brim'
  if part=='lock_key':params.update(sparse_infill_density='100%',outer_wall_speed='25,25',inner_wall_speed='30,30')
  objs.append(dict(path=str(path),count=1,filaments=[1],pos_x=[45+50*len(objs)],pos_y=[100],pos_z=[0],print_params=params))
 plates.append(dict(plate_name=name,need_arrange=False,objects=objs))
(w/'assemble.json').write_text(json.dumps(dict(plates=plates),indent=2)+'\n')

project=o/'G7_Modular_v23_U1_0.4_Snapmaker_PLA_Black.3mf'
env=dict(os.environ,LC_ALL='C')
command=[args.orca,'--debug','2','--outputdir',str(w/'export'),
         '--load-assemble-list',str(w/'assemble.json'),
         '--load-settings',str(o/'printer.json')+';'+str(o/'process.json'),
         '--load-filaments',str(o/'filament.json'),'--export-3mf',project.name]
with (w/'export.log').open('w') as log:
 subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
shutil.copy2(w/'export'/project.name,project)
if args.validate:
 (w/'validation').mkdir(exist_ok=True)
 with (w/'validation.log').open('w') as log:
  subprocess.run([args.orca,'--debug','2','--outputdir',str(w/'validation'),
                  '--allow-newer-file','--slice','0','--export-settings',str(w/'validation'/'settings.json'),str(project)],
                 env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 result=json.loads((w/'validation'/'result.json').read_text())
 assert result['return_code']==0 and len(result['sliced_plates'])==2
 assert all(not x['warning_message'] for x in result['sliced_plates']),result
 print('Both saved project plates reopened and sliced without plate warnings.')
 subprocess.run([sys.executable,str(repo/'tools'/'validate_snapmaker_orca_project.py'),'--slice-results',str(w/'validation')],check=True)
print(project)
