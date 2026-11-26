import json, subprocess
clips = {  # name: (src, start, end)
 'n1':('vo/n1.mp3',0.0,2.72), 'n2':('vo/n1.mp3',3.12,5.55), 'n3':('vo/n1.mp3',5.84,8.52),
 'n4':('vo/n1.mp3',8.85,11.99), 'n5':('vo/n1.mp3',12.15,13.32), 'n6':('vo/n1.mp3',13.64,18.96),
 'g1':('vo/g1.mp3',0.0,3.84), 'i1':('vo/i1.mp3',0.0,5.28), 'i2':('vo/i1.mp3',5.6,10.0)}
dur={}
for k,(src,a,b) in clips.items():
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',src,'-af',f'afade=t=in:d=0.03,afade=t=out:st={b-a-0.06:.3f}:d=0.06','-ar','44100','-ac','2',f'vo/{k}.wav'],check=True)
    dur[k]=b-a
AMCA=4.3  # amca repliği için ayrılan süre (ses sonra sığdırılır)
T={}; at={}
at['n1']=0.3; T['s1']=max(3.6, at['n1']+dur['n1']+0.4)
at['g1']=T['s1']+0.5; T['s2']=at['g1']+dur['g1']+0.4
at['i1']=T['s2']+0.4; T['s3']=at['i1']+dur['i1']+0.3
at['n2']=T['s3']+0.2; T['s4']=at['n2']+dur['n2']+0.3
at['a1']=T['s4']+1.0; T['s5']=at['a1']+AMCA+0.2
at['i2']=T['s5']+0.2; T['s6']=at['i2']+dur['i2']+0.2
at['n3']=T['s6']+0.1; at['n4']=at['n3']+dur['n3']+0.25; at['n5']=at['n4']+dur['n4']+0.2; T['s7']=at['n5']
T['s8']=at['n5']+dur['n5']+0.4
at['n6']=T['s8']+0.3; T['end']=T['s8']+7.0
T={k:round(v,3) for k,v in T.items()}; at={k:round(v,3) for k,v in at.items()}; at['AMCA']=AMCA
json.dump(T,open('timing.json','w'),indent=1); json.dump(at,open('vo_at.json','w'),indent=1)
print(T); print(at)
