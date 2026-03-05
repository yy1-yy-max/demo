# 3D_to_pointcloud 组件（适配 TouchDesigner 2023.12120）搭建说明

概述
- 组件目标：把任意 Mesh SOP（File SOP/Geometry）转换成点云实例（支持位置、颜色、法线、scale），并能快速导出 PLY/CSV，以及选择 Sprite / 实例化小球两种渲染方式。
- 输出：一个 COMP（命名为 `3D_to_pointcloud_comp`），内部包含：输入 SOP、Scatter（可选）、SOPtoCHOP、Null CHOP（inst_chop）、Geometry COMP（instancer）、Render TOP、Camera、Light、材质（Sprite 或 Phong）、以及用于导出的 Text DAT (Python)。

节点清单与连接（逐步）
1. 输入
   - 创建一个 COMP（Base COMP），将其命名为 `3D_to_pointcloud_comp`。
   - 该组件应有一个 SOP 输入（在组件上右侧设置 Input 让用户可以把 File SOP / Geometry 直接连接进来）。

2. 清理与采样（内部）
   - 在组件内部，把输入 SOP 先 link 到一个 `Facet SOP`（可选）用于 clean normals/weld points。
   - 如果需要从面上采样点而不是使用顶点，插入 `Scatter SOP`：
     - 参数 `nPoints` 设为组件参数（默认 50000）。
     - Scatter 输出至后续节点。
   - 可选：`Point SOP` 或 `Attribute Create SOP` 用来添加/修改 Cd、scale、id 等属性。

3. 导出到 CHOP
   - `SOP to CHOP`：连接到最终点源（Scatter 或处理后的 SOP）。
     - Method: Point Positions（导出 `tx`,`ty`,`tz`）
     - Enable Point Attributes -> 指定 `Cd`（如果需要颜色）或勾选导出所有 point attributes。
   - `Null CHOP`：把 SOPtoCHOP 输出连到一个 `Null CHOP`，命名为 `/null_inst`（或 `inst_chop`）。

4. 重命名/整理通道（可选）
   - 使用 `Shuffle CHOP` 或 `Rename CHOP` 将通道名重命名为 `tx ty tz r g b scale` 等，方便映射。

5. 实例化 Geometry COMP
   - 在组件外部或内部创建 `Geometry COMP`（命名为 `instancer_geo`）。
   - 在该 Geometry 的内部，放置一个 prototype：
     - 推荐：一个单点 SOP（用于 sprite 渲染）或低分辨球体（用于小规模的实例化）。
   - Geometry COMP 的 Instancing 页：
     - Enable Instancing: on
     - Instance CHOP: path to `/null_inst`（或你的 Null CHOP 路径）
     - Translate X / Y / Z: `tx` / `ty` / `tz`
     - Instance Color: 使用 `r g b`
     - Instance Scale: `scale`（如果存在）
   - 选择材质：
     - 大量点建议使用 Sprite MAT 或自定义 GLSL MAT（使用点精灵／贴图）。
     - 小点数量可用 Phong MAT。

6. 渲染设置
   - 创建 `Camera COMP` 与 `Light COMP`（至少一个方向光或点光）。
   - 新建 `Render TOP`，选择 Scene（包含 `instancer_geo`）并设置分辨率 & AA。

7. 导出功能（Text DAT）
   - 在组件内部放一个 `Text DAT`，把 `export_ply.py` 脚本粘贴进去（详见文件）。
   - 创建一个按钮（`Parameter COMP` 或 `Panel Execute DAT`）来触发导出脚本（例如通过 `run`）。

8. 优化建议
   - 使用 Instancing（而非复制大量网格）。
   - 对静态数据使用 `Cache CHOP`。
   - 使用 Scatter 控制点数，或在导入阶段减面。
   - 对非常大的点云（>200k）考虑 LOD / tile 分块加载。

导出 .tox（在 TouchDesigner 中）
1. 组装并调试组件后，选中 `3D_to_pointcloud_comp`。
2. 右键 -> Save Component… -> 选择保存路径 -> 会生成 `3D_to_pointcloud.tox`（二进制，需要在本地 TD 中保存）。

常见问题
- 点只显示一个：检查 Geometry COMP 的 Instancing 是否开启，Instance CHOP 路径及通道名是否匹配。
- 颜色不正确：确认 SOPtoCHOP 是否导出了 Cd，并且通道名（r,g,b 或 Cd_r 等）在 Geometry 的 Instance Color 设置中对应。
- 性能低：改用 sprite/单点实例 + shader；降低每帧数据传输量。

附：示例参数（在组件参数页创建）
- nPoints (default 50000)
- useScatter (bool)
- exportPath (string)
- spriteSize (float)
- useColor (bool)

完成后你可以右键组件 Save Component… 导出 .tox 并在其它项目直接拖入复用。