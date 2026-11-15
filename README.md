# Chinese Academic Humanizer

**先理清论证与上下文，再逐句优化中文学术表达。**

面向中文期刊论文、学位论文、毕设报告和科技报告的 AI Agent Skill。默认采用机械、机器人和航空工程论文的叙述习惯，兼顾全文深度编辑、局部保真润色，以及 Word 原生修订交付。

它不是近义词替换器，也不是 AIGC 检测规避工具。**不判断作者是否使用 AI，不承诺降低检测率，不编造数据、研究经历或参考文献。**

## 能做什么

- **先审论证，再改句子**：章节问题链 → 小节与段落职责 → 逐句改写 → 科学保真与跨章复核 → 中英文摘要同步。
- **中文工科学术语体**：用任务和约束引出方案，讲清组成、连接、动作与机理，让结果回接指标和条件。
- **不机械“去 AI”**：保留有意义的长句、正常连接词、固定学术表达和真实并列，不按词频、句长或修改数量凑指标。
- **保护科学含义**：不仅核对数字，还检查对象、物理量、条件、比较关系、因果、时序和证据层级。
- **区分交付强度**：短文本直接润色；正式 Word 修订需要范围保护、接受/拒绝验证和真实文件检查。

## 快速使用

把整个目录放入支持 `SKILL.md` 的 Agent 技能目录，或让 Agent 读取 [SKILL.md](SKILL.md)。不要只复制主文件：`references/` 中的准则是技能的一部分。

示例请求：

```text
使用 chinese-academic-humanizer，润色以下中文论文段落。
保留数据、术语、引文和适用条件，输出改写结果及主要修改理由。
```

```text
使用 chinese-academic-humanizer，参考我提供的论文文风，
对这份文稿做全文深度优化。先检查论证链和段落职责，
再逐句处理；不要只换词，不新增事实。
```

```text
使用 chinese-academic-humanizer，润色这份 Word 的第二章。
只改授权正文，保留既有批注和修订，使用原生修订，原文件不覆盖。
```

`/chinese-academic-humanizer` 是否可作为斜杠命令使用，取决于所用客户端及其技能加载方式；自然语言指定技能名也可使用。

### Hermes Agent

Hermes 的安装命令支持直接的 `SKILL.md` URL：

```bash
hermes skills install https://raw.githubusercontent.com/cmyhj/chinese-academic-humanizer/main/SKILL.md
```

安装后应确认整个技能目录及两份 `references/` 文件均已取得。若所用版本的 URL 安装器只下载主文件，请使用下面的完整仓库方式。

### 完整仓库方式（跨客户端）

```bash
git clone https://github.com/cmyhj/chinese-academic-humanizer.git
```

将克隆后的目录放入客户端实际配置的技能根目录，或直接将仓库路径交给 Agent 读取。技能根目录因客户端、操作系统和 profile 而异，请以自己的配置为准。安装器可能要求审查或确认，不建议绕过扫描或强制信任。

## 文件结构

```text
SKILL.md
references/
  default-engineering-style.md  # 默认文风、章节叙述、固定表达及来源锚点
  deep-editing-workflow.md      # 全文深度编辑与语义验收
scripts/
  validate_skill.py             # 包结构、相对引用和发布内容检查
tests/
  test_validate_skill.py
```

## 默认文风与来源

默认风格从以下公开论文提炼，重点是叙述方法，不复制研究内容：

1. 王琛、惠倩倩、张帆：《水空跨域多模态共轴无人机设计》，《航空学报》，2023，44(21)：529047。DOI：[10.7527/S1000-6893.2023.29047](https://doi.org/10.7527/S1000-6893.2023.29047)。
2. 秦日鹏、徐坤、陈佳伟等：《一种星球探测六足轮腿机器人的设计与运动规划》，《航空学报》，2021，42(1)：524244。DOI：[10.7527/S1000-6893.2020.24244](https://doi.org/10.7527/S1000-6893.2020.24244)。
3. 于淼：《固定翼无人机与四旋翼无人机对接装置及航迹规划设计》，南京航空航天大学硕士学位论文，2020年4月。

规则文件保留少量用于定位和说明写法的原文短语及 PDF 页码。**仓库不包含论文 PDF、私人文稿或实验数据，论文及短引文的权利归原权利人所有。** 这些样本不代表所有学科的唯一写法，也不意味着其每一处表述都应照搬；用户当轮样本和投稿/学校规范优先。

本项目也参考了 [academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) 的证据与保真原则，以及 [humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic) 的中文表达模式分类。取舍及许可说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 环境与限制

- **纯文本编辑**不依赖 Python 或 Microsoft Word；实际效果取决于模型能力、上下文和输入材料。
- `docx`、`word-tracked-revisions`、`pdf` 是原运行环境中的协作技能名称，**并未随本仓库打包**。其他客户端需要自行提供等效的读写、PDF 抽取、修订和验收工具；没有相应能力时不得声称已经执行文件操作。
- Word 原生打开及接受/拒绝验收通常需要安装了 Microsoft Word 的 Windows 环境和可用自动化工具。`TrackRevisions=True` 不等于所有改动已被正确记录。
- 绿色高亮默认视为作者锁定，是本技能的保护约定，不是 Word 或所有学校的通用标准；可由用户明确指定其他标记约定。
- 该技能是编辑准则，不包含通用 Word 修订执行器、AIGC 检测器或自动科学核验系统。结构测试不能证明一篇论文的语言或科学结论已经通过审查。
- 使用 AI 辅助编辑仍应遵守学校、期刊和研究机构的披露及学术诚信要求。

## 本地检查

Python 3.10+，只使用标准库：

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

检查覆盖主技能元数据、内部引用、UTF-8 和发布内容中的明显本机路径/敏感标记；不是完整安全审计，也不是文稿质量评分。

## 贡献

欢迎提交有具体上下文的表达问题、错误规则或改进建议。请优先提供虚构或已获许可的最小示例，不要在 Issue、PR 或日志中上传未公开论文、个人信息、账号凭证和敏感科研数据。请区分语言建议与需要原始证据支持的科学判断。

## License

原创规则与文档采用 [MIT License](LICENSE)。引用论文、第三方内容的原有权利不受本仓库许可证替代。
