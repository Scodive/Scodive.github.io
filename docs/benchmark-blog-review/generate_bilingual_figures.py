"""Reproduce the bilingual blog figures from public data and analytic examples."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import json
OUT=Path(__file__).resolve().parents[2]/'assets/benchmark-measurement'
font_manager.fontManager.addfont('/System/Library/Fonts/STHeiti Medium.ttc')
ZH=font_manager.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc').get_name()
BLUE,ORANGE,GREY='#235a93','#ba672f','#b8c4d2'
for lang in ['en','zh']:
    def t(en,zh): return en if lang=='en' else zh
    plt.rcParams.update({'font.family':'DejaVu Sans' if lang=='en' else ZH,'font.size':12,'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cad2dc','text.color':'#182d46','axes.labelcolor':'#384860','figure.facecolor':'#fafbfd','axes.facecolor':'#fafbfd','savefig.facecolor':'#fafbfd','svg.fonttype':'none'})
    def save(fig,name):
        fig.savefig(OUT/f'{name}-{lang}.svg',bbox_inches='tight',pad_inches=.3)
        fig.savefig(OUT/f'{name}-{lang}.png',dpi=160,bbox_inches='tight',pad_inches=.3)
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5.3))
    p=np.linspace(0,1,400)
    ax.plot(p*100,(1-.8*p)*100,label=t('Model A','模型 A'),lw=3,color=BLUE)
    ax.plot(p*100,p*100,label=t('Model B','模型 B'),lw=3,color=ORANGE)
    for v,label in [(50,t('Original mix: 50%','原组合：50%')),(200/3,t('Duplicated hard cases: 66.7%','复制难题后：66.7%'))]:
        ax.axvline(v,color=GREY,ls='--',lw=1)
        ax.text(28 if v==50 else 71, 8, t('Original mix\np = 50%', '原组合\np = 50%') if v==50 else t('Hard cases ×2\np = 66.7%', '难题记录 ×2\np = 66.7%'), va='bottom', fontsize=10)
    ax.scatter([500/9],[500/9],s=65,color='#182d46',zorder=5)
    ax.annotate(t('Tie at 55.6%','55.6% 时持平'),(500/9,500/9),xytext=(20,96),arrowprops={'arrowstyle':'->','color':'#58687b'},fontsize=12)
    ax.set(xlim=(0,100),ylim=(0,105),xlabel=t('Weight assigned to the hard-task family (%)','难题家族的权重（%）'),ylabel=t('Weighted success (%)','加权成功率（%）'))
    ax.legend(loc='upper center',bbox_to_anchor=(.70,1.02),ncol=2,frameon=False)
    ax.set_title(t('Case composition changes the winner','题目组合改变领先者'),loc='left',fontweight='bold',pad=18)
    fig.text(.13,-.03,t('Analytic example: A = 1 − 0.8p; B = p. Model behavior stays fixed.','解析例子：A = 1 − 0.8p；B = p。模型行为保持不变。'),fontsize=10)
    fig.tight_layout();save(fig,'weights')
    fig,ax=plt.subplots(figsize=(11,4.2))
    labels=t(['Defined the phenomenon','Provided validity evidence','Used uncertainty / statistical tests'],['定义所测对象','提供构念效度论据','使用不确定性估计或统计检验'])
    vals=[78.2,53.4,16.0]
    ax.barh(range(3),vals,color=[BLUE,BLUE,ORANGE],height=.48)
    ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,100)
    for i,v in enumerate(vals):ax.text(v+1.5,i,f'{v:.1f}%',va='center',fontweight='bold')
    ax.set_xlabel(t('Share of reviewed papers (%)','受审查论文中的占比（%）'))
    ax.set_title(t('From a definition to measurement evidence','从定义到测量依据'),loc='left',fontweight='bold',pad=18)
    fig.text(.01,-.03,t('Bean et al., 2025 · 445 papers · 29 experts · overlapping reporting categories','Bean 等，2025 · 445 篇论文 · 29 位专家 · 报告类别可重叠'),fontsize=10)
    fig.tight_layout();save(fig,'validity')
    fig,axs=plt.subplots(1,2,figsize=(14,5.2),gridspec_kw={'width_ratios':[1.2,1]})
    ax=axs[0];vals=[35.5,18.8,5.1,40.6]
    labels=t(['Implementation constraints','Unstated functionality','Other material issues','Outside listed categories'],['强制特定实现细节','额外未说明功能','其他实质问题','未归入上述问题'])
    ax.barh(range(4),vals,color=[ORANGE,ORANGE,ORANGE,GREY],height=.5)
    ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_xlim(0,62)
    for i,v in enumerate(vals):ax.text(v+1,i,f'{v:.1f}%',va='center')
    ax.set_xlabel(t('Share of 138 selected tasks (%)','所选 138 道题中的比例（%）'))
    ax.set_title(t('A  SWE verifier audit','A  SWE 判定器审计'),loc='left',fontweight='bold',pad=18)
    ax=axs[1];ax.barh([0,1],[20.6,54.8],color=[BLUE,GREY],height=.48)
    ax.set_yticks([0,1],t(['Binary completion','Mean partial reward'],['完整完成率','平均部分得分']));ax.invert_yaxis();ax.set_xlim(0,100)
    for i,v in enumerate([20.6,54.8]):ax.text(v+2,i,f'{v:.1f}%',va='center',fontweight='bold')
    ax.set_xlabel(t('Metric value (%)','各自指标值（%）'))
    ax.set_title(t('B  OSWorld 2.0 metrics','B  OSWorld 2.0 指标'),loc='left',fontweight='bold',pad=18)
    fig.text(.01,-.055,t('A: OpenAI, Feb 23, 2026. Selected audit; 40.6% is the residual category.\nB: Opus 4.8 · maximum thinking · batched calls · 500 steps. Checked Oct 8, 2026.','A：OpenAI，2026-02-23。选择性审计；40.6% 为剩余类别。\nB：Opus 4.8 · maximum thinking · 批量调用 · 500 步。2026-10-08 查阅。'),fontsize=10,linespacing=1.6)
    fig.tight_layout(w_pad=3);save(fig,'scoring')
    fig,ax=plt.subplots(figsize=(10,4.6));x=np.linspace(-5,5,500);p=1/(1+np.exp(-x))
    ax.plot(x,p*(1-p),lw=3,color=BLUE);ax.axvline(0,color=GREY,ls='--');ax.scatter([0],[.25],color=ORANGE,zorder=3)
    ax.set(xlim=(-5,5),ylim=(0,.28),xlabel=t('Ability θ − difficulty b (Rasch scale)','能力 θ − 难度 b（Rasch 量尺）'),ylabel=t('Item information p(1 − p)','单题信息量 p(1 − p)'))
    ax.text(-4.7,.085,t('Too hard:\nalmost all fail','过难：\n几乎都错'),fontsize=12)
    ax.text(2.6,.085,t('Too easy:\nalmost all pass','过易：\n几乎都对'),fontsize=12)
    ax.annotate('p = 0.5',(0,.25),xytext=(1,.23),arrowprops={'arrowstyle':'->','color':ORANGE})
    ax.set_title(t('The hardest item need not be the most informative','最难的题未必最有信息'),loc='left',fontweight='bold',pad=18)
    fig.text(.02,-.03,t('Analytic example · one dimension · unit discrimination · local independence','解析例子 · 单维能力 · 区分度为 1 · 局部独立'),fontsize=10)
    fig.tight_layout();save(fig,'information')
    fig,ax=plt.subplots(figsize=(10,4.6));n=np.arange(1,501)
    ax.plot(n,.99**n*100,color=BLUE,lw=3)
    for k in [20,100,299]:
        v=.99**k*100;ax.scatter([k],[v],color=ORANGE,zorder=3)
        ax.annotate(t(f'{k} tests: {v:.1f}%',f'{k} 题：{v:.1f}%'),(k,v),xytext=(k+20,v+5),fontsize=12)
    ax.axhline(5,color=GREY,ls='--')
    ax.set(xlim=(0,500),ylim=(0,100),xlabel=t('Independent tests n','独立测试次数 n'),ylabel=t('Probability of zero observed failures (%)','未观察到任何失败的概率（%）'))
    ax.set_title(t('A small mean error does not guarantee rare-failure detection','均值误差小不保证检出罕见失败'),loc='left',fontweight='bold',pad=18)
    fig.text(.02,-.03,t('Analytic example · independent, identical 1% failure probability · P(zero failures) = 0.99ⁿ','解析例子 · 独立、同分布、失败概率 1% · P(零失败) = 0.99ⁿ'),fontsize=10)
    fig.tight_layout();save(fig,'rare')
data=json.loads((OUT/'figure-data.json').read_text())
data['construction_weights']={'type':'analytic_toy_example','routine':{'n':5,'a_correct':5,'b_correct':0},'hard':{'n':5,'a_correct':1,'b_correct':5},'hard_family_crossover':5/9,'duplicated_hard_records':{'a':7/15,'b':10/15}}
data['active_figures']={'1':'weights','2':'validity','3':'scoring','4':'information','5':'rare'}
(OUT/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Generated 5 matched English/Chinese figure pairs.')
