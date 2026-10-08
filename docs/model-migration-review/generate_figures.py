from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
OUT=Path(__file__).resolve().parents[2]/'assets/model-migration'
font_manager.fontManager.addfont('/System/Library/Fonts/STHeiti Medium.ttc')
zhfont=font_manager.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc').get_name()
blue,orange,grey='#235a93','#ba672f','#c4cfda'
for lang in ['en','zh']:
 def t(en,zh):return en if lang=='en' else zh
 plt.rcParams.update({'font.family':'DejaVu Sans' if lang=='en' else zhfont,'font.size':12,'axes.unicode_minus':False,'text.color':'#182d46','axes.labelcolor':'#384860','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fafbfd','axes.facecolor':'#fafbfd','savefig.facecolor':'#fafbfd','svg.fonttype':'none'})
 def save(fig,name):
  fig.savefig(OUT/f'{name}-{lang}.svg',bbox_inches='tight',pad_inches=.25)
  fig.savefig(OUT/f'{name}-{lang}.png',dpi=160,bbox_inches='tight',pad_inches=.25)
  plt.close(fig)
 def box(ax,x,y,w,h,title,body):
  ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.03,rounding_size=.06',fc='white',ec=grey,lw=1.4))
  ax.text(x+.18,y+h-.35,title,fontsize=15,fontweight='bold',va='top')
  ax.text(x+.18,y+.2,body,fontsize=11,va='bottom',linespacing=1.55,color='#58687b')
 def arrow(ax,start,end):ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':blue,'lw':1.8})
 fig,ax=plt.subplots(figsize=(12,5.8));ax.set(xlim=(0,12),ylim=(0,5.8));ax.axis('off')
 ax.text(.1,5.35,t('A new model creates a new path through the task','新模型会走出新的任务路径'),fontsize=21,fontweight='bold')
 nodes=[(.1,t('Request +\nstate','请求与状态'),t('Same initial\ntask','相同初始任务')),(3.25,t('Model +\nharness','模型与外围系统'),t('Selects an\naction','选择动作')),(6.4,t('Tools +\nenvironment','工具与环境'),t('Action changes\nthe world','动作改变环境')),(9.55,t('Observation','新的观察'),t('Evidence for\nthe next step','下一步决策的证据'))]
 for x,title,body in nodes:box(ax,x,2.25,2.3,1.95,title,body)
 for x in [2.4,5.55,8.7]:arrow(ax,(x+.07,3.2),(x+.73,3.2))
 ax.plot([10.7,10.7,4.4],[2.15,1.3,1.3],color=blue,lw=1.8);arrow(ax,(4.4,1.3),(4.4,2.15))
 ax.text(6.0,.72,t('Different actions → different future contexts','不同动作 → 不同后续上下文'),fontsize=13,ha='center')
 ax.text(.1,.1,t('Conceptual · replay fixes the context; closed-loop evaluation lets the path change.','概念示意 · 回放固定上下文；闭环评测允许轨迹发生变化。'),fontsize=10,color='#58687b')
 save(fig,'loop')
 fig,ax=plt.subplots(figsize=(10.5,5.3));y=np.arange(3);seed=[51.7,56.2,36.5];evolved=[61.8,62.5,41.6]
 ax.barh(y-.18,seed,height=.32,color=grey,label=t('Seed harness','初始 harness'))
 ax.barh(y+.18,evolved,height=.32,color=blue,label=t('Frozen evolved harness','冻结的演化后 harness'))
 ax.set_yticks(y,['DeepSeek V4 Flash','Qwen 3.6 Plus','Gemini 3.1 Flash Lite\nPreview']);ax.invert_yaxis();ax.set_xlim(0,85)
 for i,(s,e) in enumerate(zip(seed,evolved)):
  ax.text(s+1,i-.18,f'{s:.1f}%',va='center',fontsize=11)
  ax.text(e+1,i+.18,f'{e:.1f}%  (+{e-s:.1f})',va='center',fontsize=11,fontweight='bold')
 ax.set_xlabel(t('Reported pass@1 (%) · gain in percentage points','报告的 pass@1（%）· 括号为百分点增益'))
 ax.set_title(t('Cross-model transfer without re-evolution','不重新演化，迁移到其他模型'),loc='left',fontweight='bold',pad=18)
 ax.legend(loc='lower right',frameon=False,fontsize=10)
 fig.text(.01,-.04,t('Source: AHE v3, §4.3 / Figure 3 · Terminal-Bench 2 · 89 tasks · source: GPT-5.4 high','来源：AHE v3，第 4.3 节 / 图 3 · Terminal-Bench 2 · 89 题 · 源模型：GPT-5.4 high'),fontsize=10)
 fig.tight_layout();save(fig,'transfer')
 fig,ax=plt.subplots(figsize=(8.5,5));data=np.array([[70,60],[50,75]])
 ax.imshow(data,cmap='Blues',vmin=0,vmax=100,aspect='auto')
 ax.set_xticks([0,1],t(['H_A: tuned on A','H_B: tuned on B'],['H_A：围绕 A 调优','H_B：围绕 B 调优']))
 ax.set_yticks([0,1],t(['Execute with A','Execute with B'],['用 A 执行','用 B 执行']))
 for i in range(2):
  for j in range(2):ax.text(j,i,f'{data[i,j]}%',ha='center',va='center',fontsize=30,color='white' if data[i,j]>=60 else '#182d46',fontweight='bold')
 ax.set_title(t('Model × harness: evaluate all four combinations','模型 × 外围系统：四种组合都要测'),loc='left',pad=18,fontweight='bold')
 fig.text(.02,-.04,t('Hypothetical data · replacement: −20 pp · adaptation: +25 pp · interaction: +35 pp','假设数据 · 直接替换：−20 点 · 重新适配：+25 点 · 交互项：+35 点'),fontsize=10)
 fig.tight_layout();save(fig,'matrix')
 fig,ax=plt.subplots(figsize=(11,7.2));ax.set(xlim=(0,11),ylim=(0,7.2));ax.axis('off')
 ax.text(.1,6.8,t('Stable requirements, replaceable execution choices','稳定的任务要求，可替换的执行选择'),fontsize=21,fontweight='bold')
 layers=[(4.6,t('Task contract + durable state','任务要求与持久状态'),t('Permissions · success conditions · facts · pending obligations','权限 · 成功条件 · 事实 · 未完成义务')),(2.6,t('Execution + verification','执行与验证'),t('Validated actions · idempotency · checkpoints · outcome evidence','验证动作 · 幂等性 · 检查点 · 结果证据')),(.6,t('Versioned model adapter','版本化模型适配层'),t('Messages · tool schema · context packing · model / reasoning settings','消息 · 工具 schema · 上下文组装 · 模型与推理设置'))]
 for y,title,body in layers:box(ax,.4,y,10.1,1.5,title,body)
 for y in [4.5,2.5]:arrow(ax,(5.45,y),(5.45,y-.34))
 ax.text(.4,.08,t('Proposed design · adapters preserve the contract; they do not redefine success.','建议架构 · 适配器保留任务要求，不重新定义成功。'),fontsize=10,color='#58687b')
 save(fig,'architecture')
data={'checked_on':'2026-10-08','ahe':{'source':'https://arxiv.org/html/2604.25850v3','location':'Section 4.3, Figure 3','benchmark':'Terminal-Bench 2','tasks':89,'source_model':'GPT-5.4 high','target_re_evolution':False,'models':['deepseek-v4-flash','qwen-3.6-plus','gemini-3.1-flash-lite-preview'],'seed_pass1_percent':[51.7,56.2,36.5],'evolved_pass1_percent':[61.8,62.5,41.6]},'crossed_matrix':{'status':'hypothetical, not empirical','rows':['A','B'],'columns':['H_A','H_B'],'success_percent':[[70,60],[50,75]],'replacement_pp':-20,'adaptation_pp':25,'interaction_pp':35},'cost_example':{'status':'illustrative normalized units, not provider prices','strong_route':8,'cheap_route':1,'verification':.2,'formula':'1.2 + 8*f','fallback_break_even':.85},'conceptual_figures':['loop','architecture']}
(OUT/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Generated four bilingual figure pairs')
