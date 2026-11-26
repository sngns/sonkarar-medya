// Son Karar Senin — Bölüm 3 "Sahte İsim" (2.5D piksel, 1080×1920)
import * as THREE from 'three';
import { makePost } from './post_ts.js';
import { DUR, shotAt, T } from './story.js';
import { buildCity, buildGate, buildOffice } from './sets.js';
import { drawOverlay, overlayReady, TEXTS } from './ui.js';

const W = 1080, H = 1920, Q = new URLSearchParams(location.search);
const SS = +(Q.get('ss') ?? 2);
await overlayReady();   // tabela dokuları yazı tipini kullanıyor
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById('stage').appendChild(renderer.domElement);
const camera = new THREE.PerspectiveCamera(36, W / H, .3, 2000);
const sets = { city: buildCity(), gate: buildGate(), office: buildOffice() };
const SET_OF = { hook: 'office', city: 'city', gate: 'gate', sepia: 'gate', office: 'office', door: 'office', choice: 'office' };
const post = makePost(renderer, sets.office.scene, camera, W, H, { ssaa: SS });
const V = post.vig.uniforms;
if (Q.has('nobloom')) post.bloom.enabled = false;
renderer.domElement.style.width = W + 'px'; renderer.domElement.style.height = H + 'px';

const TILT = !Q.has('notilt'), TILT_C = { city: .5 };
const _v = new THREE.Vector3();
function tiltCenter(S, shot) {
  if (TILT_C[shot.id] != null) return TILT_C[shot.id];
  const h = S.hero; if (!h || !h.root.visible) return .45;
  camera.updateMatrixWorld(); h.root.getWorldPosition(_v); _v.y += .8; _v.project(camera);
  return Math.min(.8, Math.max(.2, _v.y * .5 + .5));
}
window.DUR = DUR;
window.TEXTS = TEXTS();
window.render = t => {
  const shot = shotAt(t), sid = SET_OF[shot.id];
  if (sid) {
    const S = sets[sid]; post.dof.scene = S.scene; if (post.dof.ao) post.dof.ao.scene = S.scene;
    V.fade.value = 1; post.bloom.strength = .4; post.bloom.threshold = .9; post.bloom.radius = .7; renderer.toneMappingExposure = 1.1;
    V.warm.value = .1; V.sat.value = 1.05; V.amt.value = .6; V.contrast.value = .2;
    const ts = shot.id === 'hook' ? Math.min(t, T.freeze) : t;   // kanca: sahne donar
    S.update(ts, shot, camera, post, renderer);
    if (TILT) { post.dof.tiltAmt = 12; post.dof.tiltC = tiltCenter(S, shot); post.dof.tiltW = .09; post.dof.tiltF = .3; post.dof.maxCoc = Math.max(post.dof.maxCoc, 18); V.sat.value *= 1.12; V.contrast.value = .26; }
    if (shot.id === 'hook' && t > T.freeze) V.sat.value = .15;
    post.composer.render();
  } else { renderer.setRenderTarget(null); renderer.setClearColor('#000'); renderer.clear(); }
  if (!Q.has('noui')) drawOverlay(t, shot);
};
window.READY = true;
