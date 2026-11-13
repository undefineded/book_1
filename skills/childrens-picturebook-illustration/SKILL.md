---
name: childrens-picturebook-illustration
description: Create and revise warm cartoon children's picture-book illustrations with immersive habitats, scene-appropriate outfits, concise Chinese text, consistent bird species, and chapter-based file organization.
---

# Children's Picture-Book Illustration

Create illustrations that help a child follow, feel, and remember a story. Prioritize a clear emotional beat, readable action, warmth, and continuity over visual novelty.

## 图片生产规则与适用范围

- 用户最新指示、已确认图稿与当前项目的交付规范优先于通用模板、旧提示词和历史脚本。已确认样式与范围继续沿用，不重复征询确认。
- **最新规则：后续由用户在自己电脑上进行超分。Agent不再执行CPU或GPU超分，也不为提高场景分辨率做插值放大；新图直接保留生成时的原始像素尺寸。已有超分素材不自动删除或重做，CUnet工具保留供用户本地手动运行。**
- 进行图页生成、去字、分层或交付时，读取本Skill的[图片生产与验收规范](references/image-production.md)。规范覆盖原尺寸源图保存、透明PNG、局部修字、验收及交接；超分部分仅供用户本地参考。
- 当前雨林使用无字场景＋透明文字素材的分层PNG流程。下文雨林旧SVG/PDF段落属于历史记录；鸟类旧超清产物已按用户要求移除，只保留原图、扩图版、文稿及历史制作记录，不自动重新生成。

## Scope and defaults

- Intended readers: ages 3–8 unless the request specifies otherwise.
- Default format: 1:1 square single-page artwork, including covers and chapter openers. Only use a landscape spread when explicitly requested; for spreads keep key objects away from the gutter.
- Default visual direction: child-friendly cartoon illustration with rounded, expressive shapes, clear silhouettes, playful but restrained proportions, and watercolor-and-colored-pencil texture. Use soft natural light and avoid photorealism. Match a supplied reference or requested medium instead.
- Default palette: warm and inviting—sunlit cream, honey yellow, peach, coral, terracotta, warm leaf green, and muted sky blue—with one or two gentle cool accents for balance. Favor soft midtones, warm highlights, and comfortable contrast over neon colors, muddy grays, or a harsh dark mood.
- Preserve a calm, hopeful tone. Tension may be present, but its visual treatment must remain age-appropriate and emotionally containable.
- Warmth does not mean every page is golden sunset: use habitat-appropriate greens, blues, earth tones, moonlight, snow and indoor light while preserving a friendly, cohesive mood.
- Never add lettering, captions, logos, watermarks, or pseudo-text unless the user explicitly requests it. For a composed page, plan quiet space for the approved text. For a separate text-free scene, restore a complete natural environment without artificial typography blanks or label-shaped patches.

## Start with an illustration brief

Before generating, derive or request the smallest useful brief:

1. **Story beat:** What changes in this moment? State it in one sentence.
2. **Emotion:** Name the main feeling and a secondary feeling (for example, curious but cautious).
3. **Characters:** Record each recurring character's species/age, silhouette, proportions, face, clothing, colors, and distinctive props.
4. **Setting and time:** Identify location, season, time of day, weather, and cultural or historical details that must be accurate.
5. **Page role:** Choose establishing, discovery, action, quiet pause, transition, or closing image.
6. **Text placement:** Identify the page/area that needs quiet negative space. Keep important visual information out of that area.
7. **Production constraints:** Note orientation, trim/bleed, spread versus single page, color limits, and whether artwork must work in print.

If essential facts are absent, make a short, explicit assumption rather than inventing a complex backstory. Ask a clarifying question only when a choice would materially alter the artwork, such as the protagonist, target age, visual style, or page format.

## Design the image before prompting

Use this sequence:

1. **Choose the visual sentence.** Identify who is doing what, where, and why the child should look.
2. **Set hierarchy.** Make one focal point unambiguous; support it with gesture, contrast, framing, and leading shapes. Limit competing focal points.
3. **Make action legible.** Favor readable poses and silhouettes. Show cause and effect with props, expressions, tracks, motion cues, or reactions.
4. **Build depth simply.** Use foreground/middle-ground/background layers without crowding the scene. Let background detail reward a second look, never obscure the plot.
5. **Plan the delivery layers.** For composed pages, use a quiet physical sky, wall, snowbank or grass area for text. For separate text-free artwork, complete the habitat and put readability backgrounds on the independent lettering PNGs.
6. **Check the spread.** Keep focal action away from the center gutter; balance the two pages without making them mirror each other.

## Character continuity

For a sequence, create and maintain a character bible before generating page art. Include:

- a concise visual anchor (for example, “small russet fox, oversized teal raincoat, one cream ear tip, round amber satchel”);
- height and proportion relative to companions and objects;
- palette names or approximate colors for clothing and signature items;
- facial features and expression range;
- recurring locations and their fixed landmarks;
- explicit exclusions: no changed facial identity or eye color, no altered limb count, no age shift, no missing signature prop unless the plot calls for it. Clothing is scene-dependent: document outfit changes instead of treating one costume as permanent.

Repeat only the most important anchors in every image prompt. For revisions, say what must stay unchanged before describing the requested change.

## Active project constraints: 《羽毛图书馆：会飞的鸟类大百科》

Apply these constraints to this project. The user's latest confirmed correction takes precedence over older scripts, prompts and reference-image details. Use the latest concise layout manuscript (`40页精简排版稿.md`) and page-specific approved revisions as the current source; older long scripts are historical reference, not default typesetting copy.

- **Book format:** 40-page picture book for ages 4–8 and shared parent-child reading. All pages, front/back covers and chapter openers use 1:1 square canvases. Chapter ranges are P3–P16, P17–P24, P25–P30 and P31–P36; P1–P2 are opening material and P37–P40 are closing material.
- **Xiaoman / 小满:** a five-year-old girl with short hair and a small cloth backpack containing a notebook and colored pencils. Lock her age, face, haircut, bag and its contents across pages. Clothing and footwear MUST adapt to habitat, weather and activity: canvas/sports shoes on dry grassland, sturdy walking shoes and trousers in scrub, rain boots at streams or on muddy ground, warm clothing in cold environments, and light comfortable clothing indoors. Hats are used for sun, cold or rain as needed. Yellow rain boots are a wet-environment option, not a fixed character identifier.
- **Yuyu / 羽羽:** a hoopoe bird book sprite with golden-brown feathers. Its crest rises or relaxes to express emotion; its tail feathers resemble a bookmark. Preserve these two magical identifiers, while retaining a recognizably bird-like body and clear, child-friendly expressions. Retain the approved small rust-red book pendant on a thin neck cord, with a gold border and feather emblem. Let its position and partial occlusion follow the pose; do not silently omit it or substitute it for the bookmark tail.
- **Yuyu / 羽羽 — visual model lock:** Yuyu is always a hoopoe, never a cockatiel/parrot. It has a warm buff-to-golden-brown body, a long slender slightly down-curved black bill, broad black-and-cream zebra-barred wings, and a fan-shaped cinnamon crest with distinct black tips. The crest may open or relax with emotion; the long tail ends in a bookmark-like ribbon/feather. Keep these identifiers in every appearance. **Never give Yuyu a cockatiel's round yellow face, orange cheek patches, short hooked parrot beak, or smooth all-yellow crest.**
- **Cuckoo clue / 布谷鸟声音线索 — visual model lock:** The cuckoo is separate from Yuyu. Use the user's photograph as its species reference: smooth uncrested slate-gray head and breast, dark gray-brown folded wings, pale belly with fine dark horizontal bars, yellow eye ring, slender straight bill, long dark tail with pale spots. When singing visibly, BOTH feet grip a branch, the body sits side-on roughly horizontally, the beak opens and the head lifts slightly. It does not cling vertically to a trunk like a woodpecker. Simplify into a cute cartoon without losing these identifiers. On pages needing only a hint, use two small golden note icons, sound rings or a distant silhouette. Keep it secondary unless the story centers on it.
- **Knowledge label / 鸟类小百科:** story pages and chapter openers use a compact cream hand-journal fact sticker in a corner. Keep its exact fact text readable and outside faces, focal actions and story text. Covers, dedication and ending pages follow their specific manuscript roles (such as a feather-bookmark search prompt or parent-child task), rather than forcing a fact sticker onto every page.

## 画面叙事：小满亲历场景

- 小满应真正进入鸟类所在的环境，通过走、停、听、跨树根、扶栏、记录、侧身寻找等动作推进探索。人物的动作与视线要有明确对象，眼睛应看向正在观察的鸟或记录内容。
- 默认采用有亲历感的儿童高度中景，兼顾人物表情与环境。不要把小满缩成远处的小点，也不要把她固定放在画面边角、让鸟类排成展示队列。
- 用前景遮挡、中景行动、远景栖息地，以及道路、水流、树枝的走向建立透视。需要拉开人与鸟距离时，可让鸟停在另一棵远树上；不要仅靠极端拉远镜头来表达高度。
- 不同页面改变人物位置、动作、朝向、镜头角度和空间层次，避免反复使用同一蹲姿、同一条栈道、同一片金色芦苇或同一夕阳。
- 真实探索页使用连续的实地环境，不默认使用巨书托起场景、分框拼贴、标本式陈列或第三方讲解舞台。封面与明确需要魔法的转场可按脚本使用书本元素；图书馆整理页则表现实际桌面、书架和活动。
- 正文保留简短动作、感受或直接对话，让画面承担细节；不要为每只鸟追加旁白说明。鸟类知识放在百科贴纸中。

## 栖息地多样性与服饰适配

**优先根据鸟类活动选择环境，不为制造变化强行轮换四季。** 草原、田边、森林、灌丛、溪流、湿地、开阔湖岸、城市和室内都可以构成差异；仅在鸟类习性与情节适合时使用冰川、雪地或明显季节变化。

| 环境与活动 | 衣着、鞋帽选择 |
| --- | --- |
| 干燥开阔草地、晴天郊游 | 轻便上衣、合适长短裤、帆布鞋或运动鞋；需要时戴遮阳帽 |
| 干燥田边、石路 | 合适长袖或马甲、长裤、稳固徒步鞋；不默认穿雨靴 |
| 浓密或带刺灌丛、林下探索 | 长袖长裤、包脚步行鞋，避免裸露腿部钻刺丛 |
| 溪流、浅水、湿地泥地 | 防水雨靴和适当衣物；湿地干燥栈道可按实际情况选鞋，不一概强制雨靴 |
| 开阔湖岸、日照较强的干地 | 轻便衣物、运动鞋或徒步鞋、遮阳帽；鞋是否防水取决于站立地面 |
| 寒冷、雪地或极地 | 保暖外套、帽子、围巾及合适保暖防水鞋靴 |
| 室内整理、画画 | 轻便上衣、开衫或舒适衣裤，室内鞋或适合室内的便鞋；帽子外套可收好 |

- 小满保持5岁、脸型、短发与布包等身份特征，换衣换帽不改变人物身份。服装色彩可以变化，不固定黄色外套和黄色雨靴。
- 各页同时检查植被、地面干湿、气温、光照、服装厚度和鞋底用途是否相符。不要把不适合该环境的鸟搬到雪地或草原，只为增加视觉变化。
- 章节生成前列出各页的“栖息地／活动／镜头／衣服／鞋帽／光线”简表，检查相邻页是否过度相似。

## 精简正文与版式层级

- 正文目标为每页约20—40个汉字、2—3行，只保留一个主要动作或情绪；允许章扉、高潮和封面按必要性调整。知识细节由百科小贴士承担，不挤进正文。
- 普通内页的图内标题只保留文字，例如 `湿地里的三位邻居`，不印页码、`P19`、`19｜` 或其他页码分隔符，避免与不展示页码的非正文页形成断号。标题字高约为正文字高的115%，即比正文大一点点；不能小于正文，也不恢复为占满顶部的巨大标题。默认使用柔和古金色，正文用清晰暖深棕色，留足行距和页边距。
- 章扉使用“第几章＋章名”的独立层级，可适当放大。封面另用主书名层级；文件名中的 `P` 不自动变成印在画面中的页标题。
- 先安排人物和行动，再利用安静的天空、墙面或其他低细节区排字；必要时加轻薄米白底。不得为大段文字牺牲主画面，也不得让文字盖住脸、鸟或关键道具。
- 用户要带字图时，提示词中提供标题、正文、贴士的逐字内容和建议断行，检查漏字、重字、错字与标点。不得因默认“避免生成文字”规则而交付空白正文；用户要无字底图时才预留空白。
- 分区排版，避免将百科标题加到封底正文上。检查正文与画面是否一致，例如已删除啄木鸟的页面不再沿用啄木鸟故事文案。
- 笔记本内容也要叙事清楚：用几组可辨识的鸟形贴纸配长线、小点、彩色弧线；布谷鸟线索配两枚金色音符。录音机的真实波形和儿童自创记录符号分开表达。
- **逐页科普台词：** 用户要求四章及章内各页都设计小满与羽羽的科普对话，当前覆盖P3—P36，每页小满一次发言、羽羽一次回应，不再每章只写一组概述。对话必须落到具体鸟类、现象或结构上；羽羽解释机制、用途或区别，保留物种与个体差异等边界，不以“还有什么秘密”等泛问和知识罗列代替科普。独立台词稿见`鸟类绘本/文本/四章科普问答台词.md`，知识核对说明与来源另列；未经后续排版修订，不直接把长回答塞进现有贴纸，也不自动替换图片和原排版稿。
- **画面先于问题：** 用户进一步指出不能为讲知识而反推小满的问题。逐页先核对她此刻看见、听见、正在做什么，再用5岁孩子自然的口吻表达；不让她预知未介绍的术语、性别、祖先等结论，不捏造看不见的动作或心理。P7只有枝头布谷鸟鸣叫，不能突然问宝宝住哪里；P4不凭空引入蝙蝠，P19脚被水遮挡时不先讨论脚蹼，P35不先替松鸦安排种树意图。知识可以由羽羽在回应中适度延伸，但必须承接眼前的发现或疑问；每页的画面触发点另列供编辑核对，不作为角色台词朗读。
- **句式与语气随现场变化：** 小满可以惊呼、陈述发现、猜测、比较、试探或直接追问，不强制每句以问号收尾。羽羽自然接着解释；不能通篇用“啦？呀？”结尾，也不能机械轮换“呢、吗、吧”代替句式变化。P14采用“它们的泥窝怎么能粘在屋檐下面不掉下来呢？”，P25采用“快看，那个‘土块’动起来了！”；保留孩子的现场感和具体的科学解释。

## 人体比例、手指与接触关系（重点验收）

- **小满每只手的结构必须是四根手指加一根拇指，共五指。** 儿童卡通风格可以简化线条，但不能把人手简化成四指卡通手、连指手套或没有结构的肉团；不得出现多指、少指、融合、分叉、漂浮手指或重复手掌。
- **五指结构不等于任何角度都必须看见五个指尖。** 侧面、握持、弯曲或遮挡可以使部分手指不可见，但可见轮廓、拇指位置和遮挡顺序必须合理。不得为了数齐五指而强行摊手、画成爪形，或把被遮挡的指头补到手背、手腕及错误一侧。
- 手掌、手腕和前臂应连贯，左右手的拇指方向随朝向正确；掌背不能混淆，手腕不得异常扭折。手的大小符合5岁儿童比例，不用成人大手，也不画细长尖爪。
- **托脸／捧脸：** 掌根或掌面真实承托下颌或脸颊，弯曲的手指顺着脸侧排列；拇指位于合理的掌侧。手指不能穿入脸部、与头发融合，也不能把双手拼成一只无法辨认的手。
- **扶膝／扶栏：** 手掌顺着膝盖或栏杆表面接触，四指与拇指的走向、弯曲和受力关系自然。不得只画四根向下的手指而遗漏本应可见的侧拇指，也不得画悬空贴在物体上的手。
- **捧书／画画／持物：** 先明确哪只手支撑、哪只手翻页或握笔，再画手指包握与物体边缘的前后关系。书、笔、栏杆不得穿过手掌；物体遮挡的手指不额外补出，手指也不得与书页或笔杆融为一体。
- 身体保持5岁儿童的头身、躯干与四肢比例。检查肩、肘、腕、髋、膝、踝的连接和重心；站姿脚底落地，坐姿臀部有真实支撑，身体不得穿过椅子、桌子或栏杆。不要靠拉长上半身迁就家具；需要改为站姿等动作变化时，遵循用户确认的修订范围。
- 修手优先保持原动作、表情、服饰、道具和构图，只调整必要的掌指与接触区域。若原姿势无法合理成立，再提出或在用户授权范围内改用更自然的动作，不顺带重画整页。

## 鸟类解剖、动态与道具连续性

- 按物种检查鸟喙、翅膀、腿脚、脚趾及其可见遮挡，不把一种鸟的脚趾结构套用到所有鸟。鸵鸟每脚为一大一小两趾，无后趾；不得画成三趾、猛禽爪或蹄形。
- 飞起、停栖和奔跑须能从姿态辨认：停栖时脚趾真实抓握枝条；已离枝的起飞瞬间，双脚应与枝条有可见间隙，双翼和身体动势协调，不画成展翅却仍牢牢站在原处。不要把“刚准备起飞”与“已离枝”混用。
- 表现快速前行时，步幅、重心、衣摆、头发和道具的动势一致，不能只加速度线而主体仍静止。小满以书本滑行的已确认页面保留真实旧绿皮硬壳书的书脊、页厚与展开书页，不换成地图、纸片或滑板。
- 逐页检查羽羽的戴胜鸟特征、书签尾羽和颈间小书挂件；运动和遮挡可以改变可见程度，但不能无故丢失标志性道具。保留各页已确认的鞋型和穿着，不因局部修图恢复错误旧版。
- **平放打开的精装书：** 先按视点确定书槽、左右纸张堆、封皮与地面的关系。朝向读者的近侧前沿通常呈现层叠纸边，绿封皮贴在纸张堆下方；装订处在书槽下方自然圆转，不画成一整块竖直面板，也不把左右外封面同时正面竖起当成书页支座。保留百科应有的厚度、人物手与纸页接触、纸张透视和落地阴影。P4扩图版于2026-11-12按此修正；不将此平放结构套用到明确腾飞或翻转的魔法封面。

## 水中倒影、透视与遮挡

- 先确定水面、视点，以及人物、鸟、栏杆与栈道的前后位置，再推断倒影的大致位置、尺度和可见范围；不能把主体简单上下翻转贴进任意空白水面。
- 同一水面上的人物、鸟和栏杆倒影应服从一致的空间关系。分别核对倒影对应哪一根立柱、哪一侧横栏及其上的角色，避免把近侧栏杆的倒影误当成远侧栏杆的倒影。
- **未看见倒影不自动等于漏画。** 倒影可能被栈道、岸边、前景、版面贴纸遮挡，或落在画幅外。根据构图核对后再判断；无法确定时如实说明，不为“补齐”而凭空添加位置错误的倒影。
- 应当可见的倒影须保留相应的形体和身份特征，允许水纹造成轻微破碎、变淡和扭曲，但不能改变物种、凭空少掉关键对象，或出现与实物不对应的栏杆、肢体和道具。
- 排版时尽量让重要的倒影关系可读；知识贴纸不得无意遮住叙事重点。若需移动贴纸或调整构图才能露出倒影，先核对留白、正文与主体遮挡，并在当前授权范围内处理；不得为了补倒影擅自大幅改变布局。

## 文件命名与版本整理

### 印刷安全边距与场景扩图（2026-11-11试样）

- 用户指出现有图页文字过于贴边，要求先试做P1、P2、P3的场景扩图。延展四周真实场景，使标题、正文、完整贴纸与关键人物远离裁切边缘，维持1:1方形、原有文字及叙事关系；外沿不添加新文字，不用白框、镜像边或模糊填充替代场景。
- 本轮以原画约占新画幅宽高84%、四周各延展约8%为生成目标，实际生成需目视验收文字和贴纸余量；这些比例是试样参数，不是已确认的全书印刷规格。成品尺寸、装订方式、出血与分辨率须按实际印厂要求另行确定。
- P1—P3试样独立放在`鸟类绘本/印刷扩图试样/P1-P3/`，正式图页未替换。原图另备份到`鸟类绘本/历史版本/P1-P3-印刷扩图前-20261111/`；用户确认试样效果前，不据此批量修改其余图页。
- 用户随后认可P1—P3效果，并明确要求完成第一章剩余P4—P16；此范围已获授权，沿用同样的四周场景延展方式。新版存于`鸟类绘本/印刷扩图试样/P4-P16/`，原图备份于`鸟类绘本/历史版本/P4-P16-印刷扩图前-20261111/`，总索引为`鸟类绘本/印刷扩图试样/README.md`。保留各页此前确认的动作、服饰、文字和场景关系，不扩展至其余章节。
- 扩图不得通过重复鸟群或增加叙事主体填满新增区域，也不得把鸟类羽色扩散成整片水色。P15扩图后用户指出火烈鸟过多、湖水过红；当前修订版采用三只疏朗的火烈鸟，湖面与前景积水改为自然蓝灰色，仅保留鸟脚附近局部粉色倒影，维持右侧蓝色海面及已扩出的边距。后续以此修订为P15扩图版参考，不恢复密集鸟群或红色湖面。
- 用户随后要求新增独立`扩图版`文件夹并同步Git。用于仓库分发的P1—P16最新图片保存至`鸟类绘本/扩图版/第一章：飞向世界/`，总索引为`鸟类绘本/扩图版/README.md`；不覆盖`40页版图片`或`绘本图片`中的现有图页。Git同步当前扩图图片、索引与本规范；本地试样、历史备份、生成记录、原始生成图及下载压缩包不上传。
- 用户进一步要求第二、三、四章也扩图，本轮授权范围为P17—P36共20页。按相同方式保存至`鸟类绘本/扩图版/`下三个对应章节，保留此前已确认的手部、姿势、录音机样式、文字与鸟类数量。新增区域只延续环境，不添鸟群或其他叙事主体，不把鸟的羽色扩散成水色；特别保留P33双手在身前捧本的站姿和P36坐姿播放录音。原始生成文件及制作记录留在本地。

- 图片文件使用新稿页码和标题：`P1｜封面.png`、`P2｜扉页：会抖动的书.png`；不补零，不沿用旧16页编号冒充新页码。文件名的页码仅用于管理和排序，不渲染到图片标题中。
- 按章节归档到 `40页版图片/第一章：飞向世界/`、`第二章：寻找最美鸟鸣/`、`第三章：隐身大师与特技演员/`、`第四章：老街、山谷与奇妙的朋友/`。目录内按页码数值排序并提供索引。
- 更新已命名图片前，保留可恢复旧版（历史版本副本或已核实可恢复的Git提交），再保存新版并更新引用。原始生成文件及确认的无字源图须保留，不能只留下超分或插值成品。
- 只修改用户当前指定的页面或章节；将跨页适用的新规则记录进本Skill。不要因整理图片自动推送Git远程，除非用户要求同步上传。

### 热带雨林绘本：旧版SVG/PDF制作记录（历史）

以下记录曾执行的旧流程，仅作方法参考。用户已要求清空此前Git历史，不能依赖旧提交恢复成品。当前图页续制使用后面的PNG分层规范与根目录CUnet工具，不把旧SVG/PDF脚本作为生产默认值。

- 用户已确认P26《树叶做的午饭》的超清试样，并要求同样处理其余图页。高清成果统一存于`热带雨林绘本/超清版/`，按页分别保存；不覆盖原1254px图页、原阅读版PDF和原MD文案。
- 沿用原图构图和已确认修订。先用图像编辑工具分离旧文字，再以CUnet仅放大的2倍模型把插画升至2508×2508，独立矢量排字后导出3000×3000、300 PPI PNG及嵌入字体的PDF。不得把这一流程描述成原生3000px重绘或承诺恢复真实细节。
- 保留SVG、无字底图和超分底图，字体与授权可共享保存。当前使用霞鹜文楷，PDF应嵌入字体；逐页核对MD、SVG和PDF文字，特别检查长破折号等组合字形的显示与Unicode映射。
- 以实际导出的文字字框检查四边至少12%的余量，百科标题须落在纸片标签内，正文不能盖住人物头发、动物动作或纸片中的装饰插图。深色标签用浅色标题，夜景根据背景选择清楚的文字颜色。
- P15保留《树枝间的小跳跃》的修正站姿与自然扶栏手臂；逐手放大检查每一页，不能因去字、超分而改变五指结构、持物或扶栏接触。P37保留正式互动横线、勾选框与画图区；P38不印未确认版权占位符。
- 本轮PDF画布为254×254 mm，插画约251 PPI，文字为矢量。成品尺寸、出血、装订与印刷色彩配置仍以印厂规格为准，不自行添加生产标记或虚构出版信息。

### 热带雨林绘本：PNG分层排版

- 详细生产步骤与验收见[图片生产与验收规范](references/image-production.md)。实际完成范围从`热带雨林绘本/超清版/PNG文件清单.json`与待续制任务读取；Skill中的授权范围不代表全部图页已完成。
- 用户已确认P15《树枝间的小跳跃》和P16《远处是谁在打鼓》的试样，并授权将全书其余图页按同样方式制作，替换`热带雨林绘本/超清版/`并上传Git。试样仍独立存于`热带雨林绘本/分层排版试样/`。
- P16试验将标题正文与小百科纸签在同一张透明素材图中合画，两块独立、不接触，中间留出完整透明裁切带，再分别裁成两张PNG；保留合画素材供查看，特别核对“呜”与“鸣”等近形字。
- 用户已指定P16合画中的原手写风格。纠正错字必须在用户选定图上局部修字，保留原有笔锋、字重、字号、位置、行距与背景，不得为改字更换宋体、重排或替换整行字体。近形字须在最终PNG中放大验字，不能仅核对源字符串。“呜——呜——”的“乌”部无眼点，小百科中的“共鸣”保留“鸣”。修订图使用新文件名，避免旧版本缓存。
- 分层交付为完整无字原画、标题与正文、小百科纸签PNG；另保留标题与百科的透明合画素材。后续无字场景只交付生成原尺寸（当前一般为1254×1254），不再由Agent执行超分或额外放大；由用户本地选择超分与排版尺寸。已完成的2508px素材作为既有文件保留。文字直接渲染进PNG，不交付SVG或要求安装字体。
- 标题与正文背后加柔和米白渐变阅读底，中心保证可读性、四周自然渐隐至透明；小百科保留纸张、叶饰与边框，纸签外透明。
- 无字原画恢复完整自然场景，不能留下涂白、涂抹、模糊色块、纸签轮廓或刻意预留的文字区；保留人物身份、已确认站姿和手部、动物数量及道具。
- 封面、扉页、献辞不额外增加百科；P37独立输出可填写的观察记录，P39使用亲子延伸，P40使用回想提示。P38不输出未确认版权占位符。
- 此PNG规范取代本项目此前SVG/PDF超清交付规范。原40页正式图、MD与阅读版保留；此前Git历史已按用户要求清空，旧超清导出成果不再通过旧提交恢复。旧整书超清合集仍在本地阅读版目录保存。生成额度中断时记录逐项状态与恢复提示，保留旧页，不能将占位旧图计作新版完成。
- 共用CPU超分代码保留在根目录`CUnet/`供用户本地手动使用，构建与模型获取步骤见`CUnet/README.md`。云端雨林分层导出已停止调用CUnet，只逐字节保存原始场景并裁切文字素材。

### Per-page continuity checklist

- Keep Xiaoman's face, short hair, cloth backpack, notebook and colored pencils continuous. Verify that clothing, hat and footwear suit the depicted conditions; do not default to rain boots on dry ground.
- Make Yuyu's crest reflect its emotional state and retain the bookmark-like tail.
- Verify that Yuyu has the hoopoe's long down-curved bill, black-tipped fan crest, and barred wings; reject any cockatiel or parrot-like anatomy.
- Verify that the cuckoo, if visible, is uncrested and gray-brown with a long tail; it must never borrow Yuyu's crest, barred wings, or gold-brown palette.
- Include at most one subtle cuckoo sound clue unless the manuscript calls for more.
- Place the hand-journal bird-fact sticker in a safe corner, clear of the gutter, focal action, and text-safe area.
- Preserve left-to-right reading flow and the warm watercolor-and-colored-pencil cartoon treatment.
- Verify the square format, habitat variety, child-to-bird sightline and activity, appropriate outfit/footwear, concise text, and heading slightly larger than body text.
- Inspect each hand separately at an enlarged view: four fingers plus one thumb structurally, plausible visible/occluded digits, correct wrist connection, and natural contact with face, knees or props. Do not accept a four-digit cartoon shortcut or force all fingertips to show.
- Check child proportions, body–furniture intersections, species-specific feet and legible motion; retain approved footwear, book props and Yuyu's pendant.
- For water scenes, map reflections to their actual sources and check perspective, ripples and occlusion by the deck, foreground and fact sticker before deciding a reflection is missing.

## Page 1: cover — locked illustration brief

**Format and role:** 1:1 square cover illustration. It must feel like the inviting entrance to a bird-filled library and establish the book's magical premise at a glance.

**Scene:** Center a giant, timeworn green-covered copy of *《鸟类大百科》*, its spine facing left and cover slightly open. Its upturned pages form a pair of wings. Xiaoman stands safely on the book spine, one hand holding a page edge and the other reaching toward a drifting feather. Yuyu bursts from the book's central gap; its bookmark-like tail leaves a winding path of tiny feathers. Yuyu looks back toward the lower-right sound clue.

**Background:** Wash the background in pale golden morning light. In the far distance, include quiet silhouette cameos of a sparrow, owl, penguin, red-crowned crane, and parrot. They are an atmospheric promise of the book's contents, not competing characters.

**Cuckoo clue:** At the lower right, add a very small cuckoo silhouette with two gold musical-note symbols and a gentle sound-wave suggestion. Keep it subdued, smaller than Yuyu, and clearly secondary.

**Palette:** Old-book green, warm gold, and creamy off-white, with golden-brown accents for Yuyu. Keep the full image warm, soft, and child-friendly.

**Typography and text zones:** Use a calm, low-detail upper-left area for the title *《羽毛图书馆：会飞的鸟类大百科》*, with an aged-book gold-foil appearance. The current approved cover includes these readable lines:

```text
翻开一页，就飞进一个鸟的世界。
听，布谷鸟在叫。
```

Render the approved Chinese text when a finished cover is requested, following the text-checking rules above. Use blank zones only for a requested text-free base image.

**Knowledge marker:** In a clear cover corner, place a small “feather bookmark” sticker with the current search prompt: “羽毛和金色音符藏在哪里？跟着它们，开始探险吧。”

**Cover prompt:**

```text
1:1 square children's picture-book cover, warm watercolor-and-colored-pencil cartoon illustration. A giant timeworn green bird encyclopedia opens with wing-like pages. Five-year-old short-haired Xiaoman stands on the spine, one hand on a page and one reaching toward a feather, her cloth backpack holding notebook and pencils. Match the approved cover's outfit for this cover revision; do not carry it over as a permanent costume for other scenes. Golden-brown hoopoe Yuyu flies from the seam, with a black-tipped fan crest, curved slender bill, barred wings and bookmark tail. Pale golden dawn, tiny distant bird silhouettes. Lower-right a small uncrested gray cuckoo sings from a branch, with two gold note icons. Old-book green, warm gold and cream. Place the exact approved book title, two cover sentences and feather-bookmark search prompt in clear safe areas. No watermark, logo or photorealism.
```

## Prompt template

Write prompts in this order, using concrete and visual language:

```text
[format and page role].
Story moment: [one clear action and emotional turn].
Characters: [locked identity, scene-appropriate clothing/shoes/hat, action, expression, gaze target].
Setting: [real habitat, ground conditions, weather/time, meaningful story details].
Composition: [immersive camera angle, focal point, foreground/middle-ground/background, text-safe areas].
Art direction: [child-friendly cartoon style, medium, rounded line quality, texture, warm palette, lighting, level of detail].
Typography: [exact title, concise story with line breaks, exact fact, heading/body size ratio; or explicitly requested text-free output].
Keep: [continuity requirements, approved props and footwear; anatomically five-digit hands with natural occlusion and contact; physically coherent reflections where applicable].
Avoid: [unwanted elements, four-digit cartoon hands, extra/fused digits, distorted wrists, body–object intersections, missing signature props, misplaced reflections, accidental text, watermark, repetitive staging, clutter, unsafe or age-inappropriate material].
```

Prefer sensory specifics such as “misty pear orchard at sunrise” over abstract adjectives such as “magical.” Do not overload a prompt with incompatible styles, many simultaneous actions, or unranked details.

## 鸟类绘本：已移除的旧超清版（历史）

2026-11-13用户要求移除鸟类超清版相关产物，`鸟类绘本/超清版/`已整体移除。下列仅为历史制作记录，不表示当前仍交付这些文件，也不构成重新生成授权。原图、扩图版、文稿及共用CUnet工具保留。

- 历史高清处理范围为P1—P36最新扩图版及P40现有封底，共37张；P37—P39只有文稿。未将v2重排稿自动应用于现有图片。
- 旧产物曾独立放入`鸟类绘本/超清版/`，采用去字、CUnet两倍AI超分和矢量排字，包含3000px PNG、嵌入字体PDF、可编辑SVG及两级无字底图，现已移除。
- 延续P15三只火烈鸟和蓝灰色湖水、P24笔记本符号及P30/P33/P36已确认姿势；恢复去字时被擦除的原书脊、图书馆和早餐店文字。
- P40沿用现有图内长句，并记录与v1短稿的差别。文字实际边界四边至少12%，分别核对纸片内断行、标题对比度和字体嵌入。

## Safety and age appropriateness

- Depict children and child-coded characters with dignity, practical age-appropriate clothing, and non-sexualized presentation.
- Avoid graphic injury, gore, cruelty, terror, weapons as a focal appeal, substance use, or hopelessness. If the story includes fear or danger, soften it through distance, implication, a trusted companion, visible escape, or a reassuring resolution.
- Avoid stereotypes and caricatures. Treat culture, disability, family structure, religion, and body diversity with specificity and respect; use supplied references for culturally grounded details.
- Do not imitate a living artist's style. Translate requests into non-identifying visual qualities instead (for example, “loose watercolor washes and lively ink contours”).

## Revision protocol

When revising an image, first separate **locked** from **editable** elements.

- Locked: story beat, character identity, count of characters, composition or camera, reading direction, style, and text-safe space unless explicitly changed.
- Editable: the user's named change and only the visual consequences needed to integrate it.

Phrase the revision as: “Preserve [locked elements]. Change only [requested elements].” Recheck that the edit did not introduce extra limbs, altered faces, changed costumes, accidental text, or a shifted focal point.

## Quality gate

Before delivering, verify:

- A child can identify the main action and emotion at thumbnail size.
- The image advances the story rather than merely decorating it.
- Characters are continuous with the character bible and each other.
- Hands, limbs, eyes, clothing, and objects are coherent and usable.
- Both hands have been inspected individually at an enlarged view for five-digit structure, plausible occlusion, correct thumbs, child-sized proportions, and believable contact. A thumbnail-only review is insufficient for hand corrections.
- Bodies do not pass through furniture or props; bird feet and action match the species and story; approved footwear and Yuyu's book pendant remain continuous.
- Where water is present, reflections match their sources, perspective and occlusion. Missing reflections have been distinguished from genuinely hidden or off-canvas reflections, and fact stickers do not inadvertently conceal a key story relationship.
- The focal point is clear; background detail does not compete with it.
- Composed pages have quiet, usable text space; separate text-free scenes have complete backgrounds without leftover typography masks or sticker outlines.
- Spread artwork respects the gutter and reading direction.
- No accidental lettering, logo, watermark, visual artifact, or unsafe/age-inappropriate content is present.
- Palette, contrast, and texture support the intended feeling and reproduce plausibly in print.
- The image reads as a warm children's-book cartoon: forms are friendly and expressive, colors feel sunlit and cohesive, and no photorealistic or cold, oppressive treatment has slipped in.
- The habitat, pose, framing and light are sufficiently distinct from neighboring pages without forcing a season change or moving a bird into an unsuitable environment.
- Xiaoman's outfit and footwear suit the actual activity and ground; her face, age and short hair remain recognizable.
- Requested text is complete and legible, story remains concise, title is slightly larger than body and contains no printed page-number prefix, and story/fact content matches the final scene.
- Files use the latest page numbering, chapter folders and approved-version backups.

If any check fails, revise the prompt or image with the smallest targeted correction rather than regenerating blindly.
