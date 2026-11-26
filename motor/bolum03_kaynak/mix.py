import numpy as np, wave, json, os, subprocess
SR=44100; AT=json.load(open('vo_at.json'))
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    return a.reshape(-1,w.getnchannels()).mean(1)
bw=wave.open('bed.wav'); bed=np.frombuffer(bw.readframes(bw.getnframes()),np.int16).astype(np.float32).reshape(-1,2)/32768
N=len(bed); voice=np.zeros(N)
def put(x,at):
    i=int(at*SR); x=x[:N-i]; voice[i:i+len(x)]+=x
for k in ['n1','g1','i1','n2','i2','n3','n4','n5','n6']: put(rd(f'vo/{k}.wav'),AT[k])
if os.path.exists('vo/a1.mp3'):
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','vo/a1.mp3'],capture_output=True,text=True).stdout)
    tempo=max(1.0,d/AT['AMCA'])
    subprocess.run(['ffmpeg','-v','error','-y','-i','vo/a1.mp3','-af',f'atempo={tempo:.3f}','-ar','44100','-ac','1','vo/a1.wav'],check=True)
    put(rd('vo/a1.wav'),AT['a1']); print('amca sesi eklendi, tempo',round(tempo,3))
else: print('amca sesi YOK')
env=np.convolve(np.abs(voice),np.ones(4410)/4410,'same'); duck=1-0.55*np.clip(env/0.05,0,1)
mix=bed*0.55*duck[:,None]+voice[:,None]
mix/=np.abs(mix).max()/0.9
with wave.open('mix.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
