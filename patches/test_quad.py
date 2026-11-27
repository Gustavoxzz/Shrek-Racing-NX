import sys, pathlib, subprocess, tempfile
sys.path.insert(0,str(pathlib.Path('work/phase4-vfpu/nakagawa/tools').resolve()))
import codegen
p=pathlib.Path('work/phase4-vfpu')
for store in (False,True):
 op=(0x3e if store else 0x36)<<26 | (4<<21)
 line=codegen.normal_line(0x1234,op)
 assert 'sr_vfpu_interp' not in line
 src=r'''#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef struct {uint32_t pc,r[32],vi[128];} CpuState;
static unsigned char mem[64]; static int oor,fail;
static void sr_begin(CpuState*s,uint32_t p,uint32_t w){(void)s;(void)p;(void)w;}
static void sr_end(CpuState*s,uint32_t a,uint32_t n){(void)s;(void)a;(void)n;}
static int sr_guest_span_readable(uint32_t a,uint32_t n){return a<=64&&n<=64-a;}
static int sr_guest_span_writable(uint32_t a,uint32_t n){return sr_guest_span_readable(a,n);}
static uint32_t MEM_R32(uint32_t a){uint32_t v;memcpy(&v,mem+a,4);return v;}
static void MEM_W32_PC(uint32_t a,uint32_t v,uint32_t p){(void)p;memcpy(mem+a,&v,4);}
static void sr_oor(uint32_t a,uint32_t v,int w){(void)a;(void)v;(void)w;oor++;}
static void sr_unimplemented(uint32_t p,const char*m){(void)p;(void)m;fail++;}
static void generated(CpuState*s){ LINE }
int main(void){for(unsigned a=0;a<=65;a++){CpuState s;memset(&s,0,sizeof(s));for(int j=0;j<64;j++)mem[j]=(unsigned char)(j+1);s.pc=0x9999;s.r[4]=a;for(int j=0;j<4;j++)s.vi[j]=0x12345678+j;unsigned char old[64];memcpy(old,mem,64);oor=fail=0;generated(&s);if(a>48){if(!fail||!oor||memcmp(old,mem,64))return 1;for(int j=0;j<4;j++)if(s.vi[j]!=0x12345678u+(unsigned)j)return 2;continue;}if(oor||fail)return 3;if(s.pc != ((a&15)?0x1234:0x9999))return 4;for(int j=0;j<4;j++){uint32_t expected;memcpy(&expected,old+a+4*j,4);if(STORE){uint32_t value;memcpy(&value,mem+a+4*j,4);if(value!=0x12345678u+(unsigned)j)return 5;}else if(s.vi[j]!=expected)return 6;}}return 0;}
'''.replace('LINE',line).replace('STORE','1' if store else '0')
 with tempfile.TemporaryDirectory() as d:
  c=pathlib.Path(d)/'t.c';exe=pathlib.Path(d)/'t';c.write_text(src)
  subprocess.run(['cc','-std=c11','-Wall','-Wextra',str(c),'-o',str(exe)],check=True)
  q=subprocess.run([str(exe)],capture_output=True,text=True); print(('sv.q' if store else 'lv.q'), 'exit',q.returncode,'out-of-range diagnostics',q.stderr.count('VFPU_ACCESS_OUT_OF_RANGE')); assert q.returncode==0
