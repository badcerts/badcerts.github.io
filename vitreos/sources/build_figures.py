#!/usr/bin/env python3
"""Rebuild ten source-bound static vector plates. No experiment or network access."""
from pathlib import Path
import json, math, hashlib, textwrap, sys
sys.dont_write_bytecode=True
from format_cards_history import draw_f02, draw_f03
from format_cards_network import draw_f05
from format_cards_cutaway import draw_f06
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.font_manager import FontProperties

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'figures'
PACKET=ROOT
DATA=PACKET/'data'
def read(n): return json.loads((DATA/(n+'.public.json')).read_text())
records={r['id']:r for r in read('research-register')['records']}
results=read('results')['rows']; tracks=read('observation-tracks')['rows']
claims={r['id']:r for r in read('claim-ledger')['claims']}
INK='#163336'; SECOND='#52666A'; RULE='#D1DCD7'; TEAL='#007C83'; BLUE='#176DA5'; OCHRE='#98611A'; VIOLET='#68568D'; PAPER='#F4F5EF'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'axispl-final-figures','hatch.linewidth':0.45})
figures=[]; checks=[]
class Plate:
 def __init__(self,id,title,h):
  self.id=id;self.title=title;self.h=h
  self.fig=plt.figure(figsize=(6.5,h/72),dpi=160,facecolor='white')
  self.ax=self.fig.add_axes([0,0,1,1]);self.ax.set_xlim(0,468);self.ax.set_ylim(h,0);self.ax.axis('off');self.texts=[]
  self.text(7,7,id+'  /  '+title,11,bold=True)
  self.line(7,29,461,29,TEAL,1.1)
 def text(self,x,y,s,size=9,color=INK,bold=False,ha='left',va='top',width=None):
  if width: s='\n'.join(textwrap.fill(t,width=max(8,int(width/(size*.52))),break_long_words=False,break_on_hyphens=False) for t in s.split('\n'))
  a=self.ax.text(x,y,s,fontsize=size,color=color,fontweight='bold' if bold else 'normal',ha=ha,va=va,linespacing=1.35)
  self.texts.append(a);return a
 def line(self,x1,y1,x2,y2,color=RULE,lw=.7,style='-'):
  self.ax.plot([x1,x2],[y1,y2],color=color,lw=lw,ls=style)
 def rect(self,x,y,w,h,fill=PAPER,edge=RULE,hatch=None):
  self.ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor=edge,lw=.6,hatch=hatch))
 def arrow(self,x1,y1,x2,y2,color=SECOND):
  self.ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=8,lw=.8,color=color))
 def dot(self,x,y,c=TEAL,marker='o',fill=True):
  self.ax.plot(x,y,marker=marker,ms=5,mfc=c if fill else 'white',mec=c,mew=1,ls='none')
 def note(self,y,s):
  self.line(7,y-8,461,y-8);self.text(7,y,s,9,color=SECOND)
 def save(self,candidates,rids,unit,caption,limits,description=None,sources=None):
  self.fig.canvas.draw();ren=self.fig.canvas.get_renderer();bad=[]
  for a in self.texts:
   b=a.get_window_extent(ren); w,h=self.fig.canvas.get_width_height()
   if b.x0<0 or b.x1>w or b.y0<0 or b.y1>h:bad.append(a.get_text())
  stem=self.id.lower()+'-'+self.title.lower().replace(' ','-').replace('/','-')
  self.fig.savefig(HERE/(stem+'.svg'),format='svg',metadata={'Date':None})
  self.fig.savefig(HERE/(stem+'.png'),dpi=180)
  checks.append({'id':self.id,'text_count':len(self.texts),'minimum_font_pt':min(a.get_fontsize() for a in self.texts),'width_in':6.5,'height_in':self.h/72,'out_of_canvas_text':bad})
  src=sources or sorted({s for r in rids for s in records[r]['source_ids']})
  figures.append(dict(id=self.id,candidate_ids=candidates,title=self.title,svg=stem+'.svg',png=stem+'.png',source_ids=src,record_ids=rids,observation_unit=unit,description=description or caption,caption=caption,limits=limits))
  plt.close(self.fig)

p=Plate('F01','Availability, observation and sensitivity',391)
headers=[('Evidence family',7),('Material / custody',123),('Observed result',242),('Sensitivity / limit',355)]
for t,x in headers:p.text(x,40,t,9,bold=True)
rows=[
 ('17-file byte audit\nR05','Audit output recovered;\noriginal 17 inputs\nunavailable','Scanned anomalous\nclasses absent','Restricted features;\nordinary-space\npatterns not excluded'),
 ('Six summaries\nR06','Six retained copies\nand audit material\nrecovered privately','Anomalous bytes\nabsent; text\ndifferences reported','Collection error;\nno randomized or\ncalibrated test'),
 ('Native pair\nR18 / R33','One retained pair;\npublic token traces\nand result rows','Marked primary:\n60/93 distinct\nwindow hits','Nominal statistic;\npopulation error\nunqualified'),
 ('Historical field\nR27 / R28 / R32','Historical rows kept;\nclean exporter\nunavailable','Resource measures\nreported; usefulness\nnot measured','No causal performance\nor clean-producer\nqualification'),
 ('Keyless observer\nR31','Return retained;\nexecution and device\npeer-reported','Counts/arithmetic\nmatch supplied\nexpected output','No independent\nkey-membership\nmeasurement')]
for i,row in enumerate(rows):
 y=62+i*57
 if i%2==0:p.rect(7,y-4,454,56,fill=PAPER,edge='none')
 for j,s in enumerate(row):p.text(headers[j][1],y,s,9)
 p.line(7,y+51,461,y+51)
p.note(359,'Literal states, not a strength scale. Missing material, tested absence and\nunmeasured quantities retain different meanings.')
p.save(['C01'],['R01','R05','R06','R18','R27','R28','R31','R32','R33'],'Named evidence families; public custody differs from private recovery','Availability does not certify a claim. The audit output and six summaries were recovered privately; the 17 original audit inputs remain unavailable. Each row states what was observed and the scope in which absence is informative.','Categorical editorial summary of the specified records; no confidence score, sensitivity estimate or population conclusion.')

draw_f02(globals())

draw_f03(globals())

assert len(tracks)==512
p=Plate('F04','Recurrence at every completion position',360)
p.text(7,41,'Two retained completions; 256 token positions each. Prefix length = 4.',9,color=SECOND)
x0=85;x1=461;scale=(x1-x0)/256
styles={'unscored_prefix':('#FFFFFF',INK,'xx'),'first_window':(TEAL,TEAL,None),'first_context':(TEAL,TEAL,None),'repeat_window':('#E7ECE9',SECOND,'////'),'repeat_context':('#E7ECE9',SECOND,'////')}
from collections import Counter
actual_counts={}
for si,sample in enumerate(['clean','marked']):
 rr=sorted([r for r in tracks if r['sample']==sample],key=lambda x:x['position_zero_based']);assert [r['position_zero_based'] for r in rr]==list(range(256))
 y=88+si*104;p.text(7,y,sample.upper(),10,bold=True)
 for ti,field in enumerate(['window_class','context_class']):
  yy=y+ti*38;p.text(7,yy+15,'Window' if ti==0 else 'Context',9)
  counts=Counter(r[field] for r in rr);actual_counts[sample+'_'+field]=dict(counts)
  for r in rr:
   cls=r[field];st=styles.get(cls)
   if st is None:
    assert cls in ('repeated_window','repeated_context');st=('#E7ECE9',SECOND,'////')
   p.rect(x0+r['position_zero_based']*scale,yy,scale,12,*st[:2],hatch=st[2])
  first=counts.get('first_window',counts.get('first_context',0));repeat=252-first
  p.text(x0,yy+15,f"4 prefix  |  {first} first occurrences  |  {repeat} {'repeat' if repeat == 1 else 'repeats'}",9)
for t in [0,64,128,192,255]:
 x=x0+t*scale;p.line(x,268,x,272,SECOND);p.text(x,277,str(t),9,ha='right' if t==255 else 'center')
p.text((x0+x1)/2,295,'Completion position (zero-based; not time)',9,ha='center')
for x,lab,style in [(7,'Prefix',styles['unscored_prefix']),(114,'First occurrence',styles['first_window']),(275,'Repeated exact unit',styles['repeat_window'])]:
 p.rect(x,319,14,11,*style[:2],hatch=style[2]);p.text(x+20,318,lab,9)
p.save(['C04'],['R13','R14','R18','R20'],'512 source rows; exact completion position; separate four-token context and context-plus-target units','Every source position is represented in two aligned annotation tracks per specimen. Clean has 251 first windows and 249 first contexts; marked has 93 of each. All remaining eligible positions are repeats. The initial four positions are unscored.','Tracks show recurrence only, never secret-key membership. Deduplicating exact units does not establish independence, and position is not elapsed time. Counts are derived directly from observation-tracks.public.json.')

draw_f05(globals())

draw_f06(globals())

p=Plate('F07','Primary-key numerical comparisons',378)
p.text(7,41,'One retained pair; reported original-key rescore. Nominal z, not calibrated.',9,color=SECOND)
units=['raw_positions','first_context','first_window']; unames=['Raw positions','First context','First window']
xlo=131;xhi=445
for i,(u,uname) in enumerate(zip(units,unames)):
 yy=100+i*45;p.text(7,yy-3,uname,9,bold=True)
 vals=[]
 for sample in ['clean','marked']:
  r=next(r for r in results if r['sample']==sample and r['unit']==u and r['key_role']=='primary');vals.append(r)
 xs=[xlo+(r['nominal_z']+3)/20*(xhi-xlo) for r in vals]
 p.line(xs[0],yy,xs[1],yy,RULE,2)
 for j,(x,r) in enumerate(zip(xs,vals)):
  p.dot(x,yy,BLUE if j==0 else TEAL,marker='s' if j==0 else 'o',fill=j==1)
  p.text(x,yy-20,f"{r['nominal_z']:.4f}",9,ha='center',color=BLUE if j==0 else TEAL)
zero=xlo+3/20*(xhi-xlo);p.line(zero,70,zero,205,SECOND,.6,':')
for val in [-2,0,4,8,12,16]:
 x=xlo+(val+3)/20*(xhi-xlo);p.line(x,205,x,209,SECOND);p.text(x,214,str(val),9,ha='center')
p.text(7,217,'Nominal z',9,bold=True)
p.dot(307,243,BLUE,marker='s',fill=False);p.text(317,238,'Clean',9)
p.dot(387,243,TEAL);p.text(397,238,'Marked',9)
p.line(7,261,461,261)
p.text(7,270,'Unit',9,bold=True);p.text(164,270,'Clean hits / n',9,bold=True);p.text(322,270,'Marked hits / n',9,bold=True)
for i,(u,name) in enumerate(zip(units,unames)):
 y=290+i*21;p.text(7,y,name,9)
 for x,sample in [(164,'clean'),(322,'marked')]:
  r=next(r for r in results if r['sample']==sample and r['unit']==u and r['key_role']=='primary');p.text(x,y,f"{r['hits']} / {r['denominator']}",9)
p.note(356,'gamma = 0.25. The 93-window diagnostic does not replace the historical\n100-position minimum or qualify a new decision rule.')
p.save(['C09'],['R18','R19','R20','R33'],'Primary-key hit counts by sample and observation unit','Primary-key rows from the 18-row preserved result table. Raw marked 168/252 (z=15.2753) becomes 60/93 (z=8.8007) for first contexts and first windows. Clean denominators are 252, 249 and 251. Full-precision scores remain in results.public.json/CSV.','No calibrated p-value, confidence interval, false-positive rate or authorship probability is supplied. Rows reuse one pair; raw and deduplicated units are different. Nominal z plotted at four decimal places.',sources=['S-RESULTS','S-ENGINEERING','S-HISTORY'])

p=Plate('F08','Claim conditions and explicit exclusions',411)
p.text(7,41,'Selected ledger statements: the condition belongs to the claim itself.',9,color=SECOND)
for x,t in [(7,'Claim / status'),(171,'Evidence or satisfied scope'),(329,'Remaining condition')]:p.text(x,66,t,9,bold=True)
cr=[('L-01  BOUNDED RESULT','60/93 distinct-window hits','Original-key rescore\nS-RESULTS','One specimen;\ncalibration absent'),('L-09  BOUNDED RETURN','Keyless observer agrees','Counts + arithmetic;\nexpected output supplied','Execution/device\npeer-reported'),('L-10  EXCLUDED','Clean field provenance','Historical rows retain\ndirty-source lineage','Complete clean exporter\nand fresh export absent'),('L-12  EXCLUDED','Current Lean certification','One source-level\ncounterexample retained','No current compiled\ncertificate'),('L-13  EXCLUDED','Generic AI/person attribution','No such conclusion from\nthese observations','Required attribution\nevidence not supplied')]
for i,(id,title,evidence,cond) in enumerate(cr):
 y=91+i*51
 if i%2==0:p.rect(7,y-4,454,49,fill=PAPER,edge='none')
 p.text(7,y,id,9,bold=True,color=OCHRE if 'EXCLUDED' in id else TEAL)
 p.text(7,y+16,title,9);p.text(171,y,evidence,9);p.text(329,y,cond,9);p.line(7,y+44,461,y+44)
p.note(365,'No direct claim-to-question or claim-to-gate fields exist in the ledger.\nThis plate creates no such edges. All 14 claims, 36 questions/probes and\n64 original gates retain separate identities and histories in the report.')
p.save(['C10'],['R18','R31','R32','R33','R42'],'Five selected ledger claims, with explicit conditions and exclusions','The crosswalk summarizes explicit limits attached to L-01, L-09, L-10, L-12 and L-13. Excluded statements are shown only with their excluded status and unmet condition; the full ledger supplies all 14 claim entries.','This is a selected claim-condition table, not an inferred claim-to-gate graph or overall pass rate. No unsupported relationship among L, F, A or U identifiers is created.',sources=sorted({s for cid in ['L-01','L-09','L-10','L-12','L-13'] for s in claims[cid]['source_ids']}))

p=Plate('F09','Continuation states and finite stopping',422)
p.text(7,41,'An open question does not automatically require a new experiment.',9,color=SECOND)
states=[('CLOSED FOR THIS SCOPE','R18 keyed count; R30 historical repairs; R31 observer.','Reopen on a concrete contradiction, error or selected stronger claim.',TEAL),('UNAVAILABLE / EXCLUDED','R32 clean exporter source; stronger field claim excluded.','Retain the observation; recover source only if a new claim needs it.',OCHRE),('KNOWN UNKNOWNS','R22 output-changing coupling; R33 population calibration.','Choose a specific estimand and finite protocol before new work.',VIOLET),('OVERLOOKED AVAILABLE KNOWLEDGE','R36 overlooked records; R35 dated knowledge states.','Inspect existing archives and reconcile conflicts before collecting.',BLUE),('DISCOVERY PROBES','R37: U-01 to U-06 ask what registered explanations omit.','A probe is a search question, not a measured hidden phenomenon.',SECOND)]
for i,(head,s,next_,c) in enumerate(states):
 y=73+i*58;p.line(7,y,7,y+46,c,2);p.text(17,y,head,9,bold=True,color=c);p.text(17,y+16,s,9);p.text(17,y+31,next_,9);p.line(17,y+48,461,y+48)
p.note(383,'Select a claim -> define a discriminating observation -> fix a stop rule.\nUnavailable evidence, a negative result and abstention are legitimate endpoints.')
p.save(['C14','C15'],['R18','R22','R30','R31','R32','R33','R35','R36','R37','R42'],'Conceptual continuation states and explicitly preserved discovery probes','Closed obligations, unavailable sources, known unknowns, overlooked existing knowledge and discovery probes remain distinct. Future protocols become work only after a specific claim is selected; this map does not initiate experiments.','A conceptual process map, not a formal state machine or reachability proof. Rows do not partition all records or rank expected information gain.')

p=Plate('F10','From source field to bounded interpretation',411)
p.text(7,41,'Three evidence routes; source meaning and interpretation remain separate.',9,color=SECOND)
routes=[('R05  /  S-EARLY-AUDITS','SOURCE','17 files; specified anomalous-byte classes absent.','READING','A historical negative scan of particular uploaded copies.','CEILING','Ordinary-space encoding and unavailable original inputs remain distinct.'),('R28  /  S-FIELD-HISTORY','SOURCE','Task usefulness is null in both historical groups.','READING','No usefulness score was supplied.','CEILING','Null does not mean zero utility or confirmed useful output.'),('R31  /  S-OBSERVER','SOURCE','Returned output exactly matches supplied expected output.','READING','Counts and reported-score arithmetic agree on shared fixtures.','CEILING','No independent measurement of 60 keyed hits or authenticated execution.')]
for i,row in enumerate(routes):
 y=74+i*91;p.text(7,y,row[0],9,bold=True,color=TEAL)
 for j in range(3):
  yy=y+18+j*20;p.text(7,yy,row[1+2*j],9,bold=True,color=SECOND);p.text(75,yy,row[2+2*j],9)
 p.line(7,y+80,461,y+80)
p.text(7,359,'Correction discipline',9,bold=True)
p.text(7,376,'Recovering a record changes custody. It does not enlarge a historical\nscan\'s feature scope, supply a missing measurement or authenticate a device.',9)
p.save(['C05','C12'],['R05','R28','R31','R32'],'Three distinct source-to-interpretation routes','Each route binds a source field to its technical reading and a permitted claim. The layout is an interpretive gloss; it does not imply that unrelated observations are equivalent or that an inference is literal translation.','Retained summaries and public derivatives preserve specific claims; they do not provide independent source authentication or recover unavailable original measurements.')

assert len(figures)==10
# Verify count semantics and nominal arithmetic using frozen values only.
for r in results:
 z=(r['hits']-r['denominator']*r['gamma'])/math.sqrt(r['denominator']*r['gamma']*(1-r['gamma']))
 assert math.isclose(z,r['nominal_z'],rel_tol=1e-13,abs_tol=1e-13)
assert actual_counts['clean_window_class']['first_window']==251
assert actual_counts['marked_window_class']['first_window']==93
assert actual_counts['clean_context_class']['first_context']==249
assert actual_counts['marked_context_class']['first_context']==93
(HERE/'figures.json').write_text(json.dumps(figures,indent=2)+'\n')
(HERE/'layout_checks.json').write_text(json.dumps({'figures':checks,'numerical_checks':{'source_rows':len(tracks),'position_sets':'both exact 0..255','result_rows_arithmetic_verified':len(results),'generated_pairs':read('results')['generated_pairs'],'recurrence_counts':actual_counts},'input_sha256':{n:hashlib.sha256((DATA/n).read_bytes()).hexdigest() for n in ['observation-tracks.public.json','results.public.json','research-register.public.json','claim-ledger.public.json']}},indent=2)+'\n')
print(json.dumps(checks,indent=2))
