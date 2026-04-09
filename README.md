<div align="center">

<img src="assets/mempalace_logo.png" alt="MemPalace" width="280">

# MemPalace

### 面向中文内容与中文创作场景优化的本地 AI 记忆系统 Fork

[**中文 README**](README.md) | [English README](README.en.md)

</div>

---

> [!IMPORTANT]
> 这是一个 **对中文工作流做了专门优化的 MemPalace Fork**。
>
> 它保留了上游的核心架构和原始文本存储思路，同时额外增强了：
>
> - 中文文本与中英混合工作流
> - 中文小说 / 世界观 / 角色 / 大纲 / 正文等创作目录识别
> - 中文决策、偏好、里程碑、问题、情绪等记忆提取
> - 更适合本地中文写作项目的启发式分类
>
> 这个 Fork 的原则是 **增量增强，不破坏英文能力**：
>
> - 英文支持仍然保留
> - 原有英文启发式没有被删除
> - 目标是提高中文检索与中文创作体验，而不是把项目改成“只支持中文”

## 这是什么

MemPalace 是一个本地运行的 AI 记忆系统。它不依赖云端服务，不需要把你的对话、项目、笔记上传出去，而是把原始内容存进本机的 ChromaDB，并通过一套“宫殿式”结构把它组织起来，让 AI 后续能够重新找到这些信息。

和很多“先总结、再决定什么值得记住”的方案不同，MemPalace 的核心思路是：

- **尽量保留原文**
- **不要过早丢弃上下文**
- **在检索阶段解决“怎么找到”**

简单说，就是“先存，再找”，而不是“先压缩，再赌总结没丢东西”。

## 这个 Fork 适合谁

这个版本尤其适合以下场景：

- 中文聊天记录归档
- 中文工程笔记、文档、会议记录
- 中文小说写作项目
- 世界观、角色、设定、大纲、章节、正文管理
- 中英混合的本地知识库

如果你的主要使用场景是中文写作、中文项目研发或者中文资料检索，这个 Fork 会比上游默认版本更合适。

## 这个 Fork 做了什么优化

目前已经补进去的中文增强主要包括：

### 1. 中文房间识别

除了原来的英文目录识别，这个 Fork 现在还能更好地识别这类中文目录或主题：

- `故事` / `小说`
- `设定` / `世界观`
- `人物` / `角色`
- `剧情` / `大纲`
- `正文` / `章节`
- `记忆`
- 以及常见中文工程目录，如 `前端` / `后端` / `文档` / `测试` / `配置`

### 2. 中文记忆提取

在 `general extractor` 里额外加入了中文启发式识别，用来提取：

- 决策
- 偏好
- 里程碑
- 问题
- 情绪内容
- 已解决问题

这意味着它对中文对话、中文创作讨论、中文项目记录的结构化提取会比原版更稳。

### 3. 中文创作场景更友好

对小说项目来说，很多信息不是“代码知识”，而是：

- 角色设定
- 关系变化
- 世界观规则
- 伏笔与回收点
- 章节规划
- 风格与写法约束

这个 Fork 已经在目录识别和文本提取层面，朝这些场景做了适配。

## 核心特性

### 原文存储

MemPalace 默认会把原始文本直接存储到 ChromaDB，而不是先做摘要再入库。这样做的好处是：

- 保留原始语境
- 保留“为什么”
- 避免总结阶段丢掉关键细节

### 宫殿结构

MemPalace 用一套层级结构组织记忆：

- **Wing**：一个项目、一个人、一个主题
- **Room**：该 Wing 下的具体主题
- **Hall**：跨主题的记忆类型
- **Closet**：指向内容的摘要层
- **Drawer**：原始文本内容

这套结构的价值不只是“看起来漂亮”，而是能把检索范围收窄，让 AI 更快、更准确地找到相关内容。

### 本地运行

- 无需外部 API
- 数据不离开你的机器
- 可自定义、可自托管、可离线组合本地模型

### MCP 工具支持

MemPalace 提供 MCP Server，可以接进 Claude Code、ChatGPT 桌面端、Cursor、Gemini 等支持 MCP 的工具链。

### 知识图谱与时间有效性

除了向量检索外，MemPalace 还提供本地知识图谱，用来表达：

- 谁参与了什么
- 某个事实从什么时候开始成立
- 什么时候失效
- 某个人或项目的时间线变化

## 快速开始

```bash
pip install mempalace

# 初始化一个项目
mempalace init ~/projects/myapp

# 挖掘项目文件
mempalace mine ~/projects/myapp

# 挖掘聊天记录
mempalace mine ~/chats/ --mode convos

# 自动提取决策 / 里程碑 / 问题 / 情绪等信息
mempalace mine ~/chats/ --mode convos --extract general

# 搜索历史内容
mempalace search "为什么当时改用 GraphQL"

# 查看宫殿状态
mempalace status
```

MemPalace 主要有三种挖掘模式：

- `projects`：项目文件、代码、文档、笔记
- `convos`：聊天记录、对话导出
- `general`：按启发式提取决策、偏好、问题、里程碑、情绪

## 中文优先的推荐用法

如果你主要做中文写作、中文知识管理或中文项目开发，建议这样使用：

### 小说 / 长篇创作

可以把以下目录或文件放到同一个项目下，然后直接 `mine`：

- `设定`
- `世界观`
- `人物`
- `剧情`
- `大纲`
- `正文`
- `章节`
- `记忆`

这样做的好处是，后续你可以按主题检索：

- 某个角色之前的设定
- 某条伏笔第一次出现在哪里
- 哪一章修改过世界观规则
- 某次讨论里最终决定保留了哪种写法

### 中英混合工程项目

如果项目同时包含：

- 中文会议记录
- 英文代码注释
- 中文研发决策
- 英文技术文档

这个 Fork 会比只针对英文优化的默认启发式更实用，因为它能更好地处理混合脚本内容。

## 和 Long-Novel-GPT 这类项目怎么配合

对长篇写作项目，建议把 MemPalace 当作 **长期检索记忆层**，而不是直接替换项目自己的压缩记忆文件。

推荐分层：

- **L0 / L1**：项目内现有的 `series_bible_short`、`story_memory`
- **L2 / L3**：MemPalace 的长期检索与原文回溯

这样可以同时保留：

- 压缩后的 prompt 友好记忆
- 原始资料的可追溯检索

也就是说，最佳做法通常不是“二选一”，而是并存。

## 如何实际使用

### 1. 配合 Claude Code

```bash
claude plugin marketplace add milla-jovovich/mempalace
claude plugin install --scope user mempalace
```

重启 Claude Code 后，MemPalace 的工具就可以被调用。

### 2. 配合 MCP 客户端

```bash
claude mcp add mempalace -- python -m mempalace.mcp_server
```

然后你的 AI 就可以直接调用类似这样的工具：

- `mempalace_status`
- `mempalace_search`
- `mempalace_list_wings`
- `mempalace_list_rooms`
- `mempalace_kg_query`
- `mempalace_add_drawer`

### 3. 配合本地模型

如果你用的是本地 LLM，而它暂时不支持 MCP，可以这样做：

```bash
mempalace wake-up > context.txt
```

把 `context.txt` 放进系统提示词，作为模型的基础记忆层。

或者：

```bash
mempalace search "auth decisions" > results.txt
```

把检索结果塞回 prompt，让本地模型基于真实历史内容回答。

## 宫殿结构解释

### Wing

一个项目、一个人物、一个主题，对应一个 Wing。

### Room

Wing 内的具体主题，例如：

- `auth-migration`
- `worldbuilding`
- `characters`
- `plot`

### Hall

一种跨 Wing 的记忆类型，比如：

- `hall_facts`
- `hall_events`
- `hall_discoveries`
- `hall_preferences`
- `hall_advice`

### Closet

指向原始内容的摘要层。

### Drawer

真实原文。真正的内容最终在这里。

## AAAK 是什么

AAAK 是 MemPalace 提供的一种压缩记忆方言，目标是在规模很大时，用更紧凑的方式表达重复出现的实体与关系。

需要注意的是：

- AAAK 不是默认存储格式
- 默认高分检索结果来自 **raw verbatim mode**
- AAAK 目前更适合作为压缩层，而不是替代原始存储

如果你想看更完整、偏原作者口径的 AAAK 说明和 benchmark 细节，请直接看：

- [English README](README.en.md)

## 语言能力说明

这个 Fork 的定位不是“中文专用版”，而是“中文优先优化版”。

也就是说：

- 中文能力加强了
- 中英混合场景更稳了
- 英文能力仍然保留

目前做的是启发式和目录识别层的增强。如果你后续要把中文语义检索效果再往上推，建议继续搭配更适合中文的 embedding 方案。

## 常用命令

```bash
# 初始化
mempalace init <dir>

# 挖掘项目
mempalace mine <dir>

# 挖掘聊天记录
mempalace mine <dir> --mode convos

# 搜索
mempalace search "query"
mempalace search "query" --wing myapp
mempalace search "query" --room worldbuilding

# 唤醒记忆层
mempalace wake-up

# 查看状态
mempalace status
```

所有命令都支持：

```bash
--palace <path>
```

用于覆盖默认宫殿目录。

## 文档说明

当前文档组织建议如下：

- 中文默认入口：[`README.md`](README.md)
- 英文说明：[`README.en.md`](README.en.md)

如果你更关心以下内容，建议直接跳英文版：

- 完整 benchmark 描述
- AAAK 细节与问题说明
- 更完整的项目结构介绍
- 上游原始文档风格

## 许可证

MIT，详见 [LICENSE](LICENSE)。

## 致谢

- 原项目与整体架构思路来自上游 MemPalace
- 本 Fork 重点补的是中文工作流、中文创作目录、中文记忆提取与中文优先使用体验

