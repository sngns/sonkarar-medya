import json, subprocess
TEMPO=1.08
clips = {  # name: (src, start, end)
 'n1':('vo/n1.mp3',0.0,3.95), 'n2':('vo/n1.mp3',5.05,10.05), 'n3':('vo/n1.mp3',11.05,13.68), 'n4':('vo/n1.mp3',14.55,19.6),
 'a1':('vo/a1.mp3',0.15,5.12), 'g1':('vo/g1.mp3',0.0,4.85), 'g2':('vo/g1.mp3',5.6,12.0)}
dur={}
for k,(src,a,b) in clips.items():
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',src,'-af',f'atempo={TEMPO},afade=t=in:d=0.03,afade=t=out:st={(b-a)/TEMPO-0.06:.3f}:d=0.06','-ar','44100','-ac','2',f'vo/{k}.wav'],check=True)
    dur[k]=(b-a)/TEMPO
T={}; at={}
t=0.25; at['n1']=t; t+=dur['n1']+0.25; T['s1']=t
at['a1']=t+0.2; T['cardAt']=at['a1']+(2.3-0.15)/TEMPO; t=at['a1']+dur['a1']+0.3; T['s2']=t
at['n2']=t+0.5; t=at['n2']+dur['n2']+0.35; T['s3']=t
at['n3']=t+0.35; t=at['n3']+dur['n3']+0.2; T['s4']=t
at['g1']=t+0.1; T['notice']=at['g1']+1.95/TEMPO; t=at['g1']+dur['g1']+0.2; T['s5']=t
at['g2']=t+0.1; t=at['g2']+dur['g2']+0.2; T['s6']=t
at['n4']=t+0.1; T['s7']=at['n4']+(18.27-14.55)/TEMPO; t=at['n4']+dur['n4']+0.3; T['s8']=t
T['end']=T['s8']+6.5
T={k:round(v,3) for k,v in T.items()}
json.dump(T,open('timing.json','w'),indent=1); json.dump({k:round(v,3) for k,v in at.items()},open('vo_at.json','w'),indent=1)
print(T); print(at)
