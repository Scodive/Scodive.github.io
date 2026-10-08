"""Reproduce the blog's public-data and explicitly illustrative figures.

Run with a Python environment containing matplotlib and numpy.
No unpublished experiment data is used.
"""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets/benchmark-measurement'
OUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont('/System/Library/Fonts/STHeiti Medium.ttc')
plt.rcParams.update({
    'font.family': font_manager.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc').get_name(),
    'font.size': 12, 'axes.unicode_minus': False, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.edgecolor': '#cad2dc', 'axes.labelcolor': '#384860',
    'text.color': '#172a43', 'xtick.color': '#52637a', 'ytick.color': '#52637a',
    'figure.facecolor': '#fafbfD', 'axes.facecolor': '#fafbfD', 'savefig.facecolor': '#fafbfD',
})
BLUE, ORANGE, GREY = '#235a93', '#ba672f', '#b8c4d2'

def save(fig, name):
    fig.savefig(OUT / f'{name}.svg', bbox_inches='tight', pad_inches=.25)
    fig.savefig(OUT / f'{name}.png', dpi=180, bbox_inches='tight', pad_inches=.25)
    plt.close(fig)

fig, ax = plt.subplots(figsize=(13, 6.2))
ax.set(xlim=(0, 13), ylim=(0, 6.2)); ax.axis('off')
nodes = [
    (0.15, 3.65, '01  评测目的', '要支持哪一种判断？\n部署、比较、诊断或风险筛查'),
    (4.5, 3.65, '02  题目构建', '抽样、生成与验收\n代表性、可解性、难度范围'),
    (8.85, 3.65, '03  实际执行', '目标挑战真的发生了吗？\n触达、绕过、前序阻断、缺测'),
    (8.85, 1.15, '04  评分证据', '判对行为与终态了吗？\n合法替代解与错误解检查'),
    (4.5, 1.15, '05  题集组合', '有限预算怎样分配？\n多目标覆盖、冗余、成本'),
    (0.15, 1.15, '06  结论与迁移', '结论适用于谁、何时？\n新模型、任务分布与版本'),
]
for x,y,t,b in nodes:
    ax.add_patch(FancyBboxPatch((x,y),4,1.65,boxstyle='round,pad=0.06,rounding_size=.08',fc='white',ec='#cbd5e1',lw=1.2))
    ax.text(x+.22,y+1.18,t,fontsize=16,fontweight='bold')
    ax.text(x+.22,y+.65,b,fontsize=12,linespacing=1.65,va='center',color='#52637a')
for a,b in [((4.23,4.5),(4.42,4.5)),((8.58,4.5),(8.77,4.5)),((10.85,3.5),(10.85,2.94)),((8.76,2),(8.57,2)),((4.42,2),(4.22,2))]:
    ax.annotate('',b,a,arrowprops={'arrowstyle':'->','color':BLUE,'lw':2})
ax.text(.15,5.85,'从“有一批题”到“支持一个判断”',fontsize=22,fontweight='bold')
ax.text(.15,.3,'概念示意 · 每一条连接都需要证据；任何一环做得好，都不能代替其余环节。',fontsize=12,color='#52637a')
save(fig,'measurement-chain')

fig,ax=plt.subplots(figsize=(11,4.5))
labels=['定义了所测对象','提供构念效度论据','使用不确定性估计或统计检验']
vals=[78.2,53.4,16.0]
ax.barh(range(3),vals,color=[BLUE,BLUE,ORANGE],height=.47)
ax.set_yticks(range(3),labels); ax.invert_yaxis(); ax.set_xlim(0,100)
ax.set_xlabel('所审查 benchmark 论文中的占比（%）')
ax.xaxis.grid(True,alpha=.15);ax.set_axisbelow(True)
for i,v in enumerate(vals):ax.text(v+1.6,i,f'{v:.1f}%',va='center',fontweight='bold',fontsize=15)
ax.set_title('定义、效度论证与比较方法，是不同的报告环节',loc='left',pad=20,fontweight='bold')
fig.text(.01,-.025,'来源：Bean et al., 2025，445 篇论文 / 29 位专家。三项可重叠，不是互斥分类；审查论文报告，未复跑全部评测。',fontsize=10,color='#52637a')
fig.tight_layout();save(fig,'validity-audit')

fig,axs=plt.subplots(1,2,figsize=(13,5.2),gridspec_kw={'width_ratios':[1.15,1]})
ax=axs[0]
vals=[35.5,18.8,5.1,40.6]
labels=['强制特定实现细节','测试额外未说明功能','其他实质问题','未归入上述问题']
ax.barh(range(4),vals,color=[ORANGE,ORANGE,ORANGE,GREY],height=.52)
ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_xlim(0,60)
for i,v in enumerate(vals):ax.text(v+1,i,f'{v:.1f}%',va='center')
ax.set_xlabel('被选择审计的 138 题中的比例（%）')
ax.set_title('A  评分器能否拒绝正确解？',loc='left',pad=16,fontweight='bold')
ax=axs[1]
ax.barh([0,1],[20.6,54.8],height=.48,color=[BLUE,GREY])
ax.set_yticks([0,1],['完整完成率','平均部分得分']);ax.invert_yaxis();ax.set_xlim(0,100)
for i,v in enumerate([20.6,54.8]):ax.text(v+2,i,f'{v:.1f}%',va='center',fontweight='bold')
ax.set_xlabel('各自指标值（%）；并非可相加的两部分')
ax.set_title('B  做完一些步骤等于交付了吗？',loc='left',pad=16,fontweight='bold')
fig.text(.01,-.045,'A：OpenAI SWE-bench Verified 审计（2026-02-23）；40.6% 为 100−59.4，非“全部正确”认证。\nB：OSWorld 2.0 项目页，Opus 4.8 / maximum thinking / batched calls / 500 steps；2026-10-08 查阅。',fontsize=10,color='#52637a',linespacing=1.6)
fig.tight_layout(w_pad=3);save(fig,'scoring-evidence')

fig,ax=plt.subplots(figsize=(10,4.8))
x=np.linspace(-5,5,500);p=1/(1+np.exp(-x));info=p*(1-p)
ax.plot(x,info,color=BLUE,lw=3)
ax.axvline(0,color=GREY,ls='--');ax.scatter([0],[.25],color=ORANGE,zorder=3)
ax.set(xlim=(-5,5),ylim=(0,.28),xlabel='模型能力 θ − 题目难度 b（Rasch 潜在量尺）',ylabel='单题 Fisher 信息量 p(1−p)')
ax.text(-4.8,.08,'过难：几乎都错\n能力估计的信息少',fontsize=12)
ax.text(2.5,.08,'过易：几乎都对\n能力估计的信息少',fontsize=12)
ax.annotate('匹配该能力区间\np = 0.5',xy=(0,.25),xytext=(1,.23),arrowprops={'arrowstyle':'->','color':ORANGE},fontsize=12)
ax.set_title('最难的题，不一定最能区分当前模型',loc='left',pad=18,fontweight='bold')
fig.text(.01,-.035,'解析示意，非拟合实验：单维 Rasch / 区分度固定为 1 / 局部独立。信息量针对能力估计，不等于风险或业务价值。',fontsize=10,color='#52637a')
fig.tight_layout();save(fig,'item-information')

fig,ax=plt.subplots(figsize=(10,4.8))
n=np.arange(1,501);miss=.99**n*100
ax.plot(n,miss,color=BLUE,lw=3)
for k in [20,100,299]:
 v=.99**k*100;ax.scatter([k],[v],color=ORANGE,zorder=5)
 ax.annotate(f'{k} 题：{v:.1f}%',(k,v),xytext=(k+18,v+5),fontsize=12)
ax.axhline(5,color=GREY,ls='--');ax.set(xlim=(0,500),ylim=(0,100),xlabel='独立抽取题目数 n（题）',ylabel='一次失败也没观察到的概率（%）')
ax.set_title('估计平均成绩与发现罕见问题，需要不同的样本设计',loc='left',pad=18,fontweight='bold')
fig.text(.01,-.035,'解析示意：每题独立、同分布且真实失败概率为 1%，P(零失败) = 0.99ⁿ。真实 Agent 任务不一定满足这些假设。',fontsize=10,color='#52637a')
fig.tight_layout();save(fig,'rare-risk')

fig,ax=plt.subplots(figsize=(12,5.3));ax.axis('off');ax.set(xlim=(0,12),ylim=(0,5.3))
ax.text(.1,4.95,'相同工具、相同成功分数，可以提供不同的测量证据',fontsize=21,fontweight='bold')
headers=['任务表面','执行中需要处理的差别','需要验证的证据']
for x,h in zip([.2,3.65,8],headers):ax.text(x,4.25,h,fontsize=14,color=BLUE,fontweight='bold')
rows=[('直接创建提醒','所需时间已写在当前请求中','正确写入 ≠ 测到旧反馈保留'),('更新已有提醒','旧记录与新指令存在冲突','读取了哪些版本？最终遵循哪一个？'),('临时查询失败后更新','查询失败是可恢复的','有没有遇到故障？是否恢复后完成？')]
for i,(a,b,c) in enumerate(rows):
 y=3.25-i*1.1;ax.axhline(y+.6,color='#dce2ea',lw=1)
 for x,txt in zip([.2,3.65,8],[a,b,c]):ax.text(x,y,txt,fontsize=12,va='center')
ax.text(.2,.25,'假想案例，仅用于解释设计：没有使用未公开实验题目、响应数值或选题结果。',fontsize=11,color='#52637a')
save(fig,'case-evidence')

data={
 'checked_on':'2026-10-08',
 'validity_audit':{'n_articles':445,'expert_reviewers':29,'defined_phenomenon_pct':78.2,'validity_evidence_pct':53.4,'uncertainty_or_statistical_tests_pct':16.0,'source':'https://arxiv.org/html/2511.04703v1'},
 'swe_audit':{'selected_n':138,'full_n':500,'material_issues_pct':59.4,'narrow_tests_pct':35.5,'wide_tests_pct':18.8,'other_pct':5.1,'source':'https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/'},
 'osworld':{'version':'2.0','model':'Claude Opus 4.8','configuration':'maximum thinking, batched tool calls, 500 steps','binary_completion_pct':20.6,'partial_score_pct':54.8,'source':'https://osworld-v2.xlang.ai/'},
 'analytic_examples':{'not_empirical':True,'rare_failure_rate':.01,'zero_failures_probability':{str(k):.99**k for k in [20,50,100,299]},'minimum_n_for_95pct_detection':math.ceil(math.log(.05)/math.log(.99))}
}
(OUT/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Wrote 6 SVG + 6 PNG figures and their public/analytic data.')
