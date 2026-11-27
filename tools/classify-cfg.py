import mmap,json,collections,sys
from pathlib import Path
p=Path(sys.argv[1])
with p.open('rb') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
 def arr(key):
  pos=m.find(('"'+key+'":[').encode()); assert pos>=0,key
  pos+=len(key)+3
  # JSON compact array may contain nested arrays; parse bounded slice using successive expansions.
  size=262144
  while True:
   try: return json.JSONDecoder().raw_decode(m[pos:pos+size].decode())[0]
   except json.JSONDecodeError:
    size*=2
    if size>67108864: raise
 unowned=arr('unowned_executable'); edges=arr('unresolved_indirect_edges'); conflicts=arr('ownership_conflicts'); intervals=arr('executable_intervals'); jump=arr('jump_table_ownership')
 start=m.find(b'"instructions":['); end=m.find(b'"interior_entries":',start); assert 0<start<end
 def ins(address):
  pattern=('"address":%d,' % address).encode(); pos=m.find(pattern,start,end)
  if pos<0: return None
  assert m[pos-1:pos]==b'{' 
  return json.JSONDecoder().raw_decode(m[pos-1:pos+65536].decode())[0]
 cache={}
 cursor=start
 for address in sorted(set(unowned) | {e["source"] for e in edges}):
  pattern=("\"address\":%d," % address).encode(); pos=m.find(pattern,cursor,end)
  if pos<0: raise ValueError(address)
  assert m[pos-1:pos]==b"{"
  cache[address]=json.JSONDecoder().raw_decode(m[pos-1:pos+65536].decode())[0]
  cursor=pos+len(pattern)
 nodes=[cache[a] for a in unowned]; enodes=[cache[e["source"]] for e in edges]
 assert all(x is not None for x in nodes+enodes)
 def summary(ns):
  return {'opcodes':dict(collections.Counter(n['opcode']['mnemonic'] for n in ns).most_common()), 'classifications':dict(collections.Counter(n['classification'] for n in ns)), 'delay_slots':sum(n['delay_slot_of'] is not None for n in ns), 'terminators':dict(collections.Counter(n.get('terminator','none') for n in ns))}
 result={'unowned_count':len(unowned),'unowned':summary(nodes),'indirect_count':len(edges),'indirect_detail':dict(collections.Counter(e.get('detail') for e in edges)),'indirect_sources':summary(enodes),'conflicts_count':len(conflicts),'jump_table_candidates':len(jump),'jump_table_targets_with_owner':sum(bool(j['owners']) for j in jump),'executable_intervals_count':len(intervals)}
 print(json.dumps(result,indent=2))




