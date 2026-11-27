from pathlib import Path
import re,sys,collections
sys.path.insert(0,str(Path('work/phase4-vfpu/nakagawa/tools').resolve()))
import codegen
words=set(); counts=collections.Counter()
for p in Path('outputs/Shrek-Racing-NX/generated/shrek-attempt').glob('*.c'):
 for l in p.open(encoding='utf8'):
  for x in re.findall(r'sr_vfpu_interp\(s,0x([0-9a-f]+)u\)',l): words.add(int(x,16));counts[int(x,16)>>26]+=1
for w in words:
 effect,_,_=codegen.vfpu_effect(0x1234,w)
 assert 'sr_vfpu_interp' not in effect,hex(w)
print('unique opcodes',len(words),'sites',sum(counts.values()),'all emitter outputs interpreter-free')
