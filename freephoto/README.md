# FreePhoto · 成熟开源项目改造版

FreePhoto 是在 [MAZANOKE](https://github.com/civilblur/mazanoke) 基础上做的中文品牌化改造，保留原始开源图像处理引擎，而非重新实现压缩算法。

- **上游基线**：`civilblur/mazanoke` 固定提交 `ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b`（v1.1.7）。
- **开源协议**：GNU GPL-3.0。所有修改版仍需遵守 GPL-3.0；保留原作者、原许可证、第三方组件的版权声明。
- **原始核心功能**：批量图片压缩、目标文件大小、尺寸限制、JPG/PNG/WebP/ICO 输出、HEIC/AVIF/TIFF/GIF/SVG 等输入、EXIF 信息清除、离线 PWA。
- **改造内容**：FreePhoto 品牌、暖白森林绿视觉、部分中文界面、本地优先隐私说明、子目录部署适配。
- **注意**：首版沿用上游标识图标及相关资产。正式独立品牌发布前建议更换 Logo、favicon、应用图标与 OG 图，并完成真实浏览器功能测试。

## 构建方法

```bash
python3 build.py
python3 -m http.server 8765 -d dist
# 打开 http://localhost:8765/
```

命令会从官方 GitHub 下载上游仓库并固定到锁定提交；生成的 `dist/` 包含全部静态站点文件和完整上游版权信息。构建过程需要互联网；生成后图片处理在浏览器本地执行。**不要把 `dist/` 的源码与第三方组件许可证移除后再发布。**

如已手动下载上游源码，也可运行：

```bash
python3 build.py --from-source /path/to/mazanoke --out dist
```

## 已知限制

- 中文界面覆盖静态文案，部分动态消息仍可能显示英语。
- 官方原版的功能、设备限制与格式兼容性仍然适用；部分输入格式只支持静态首帧。
- 目前未经过 iOS Safari、Android、Windows、macOS 的完整端到端回归；正式上线前必须使用真实图片检查编码、EXIF/GPS、ZIP 下载和离线 PWA。
- 不涉及图片云端上传；但站点部署方应检查第三方分析脚本、HTTP headers 与独立部署域名。

## 商业模式

保持图片工具免费开源；站点底部可以克制地说明作者 AI 酋长 Andy 及个人 AI+IP 服务，但不得向用户隐瞒上游来源。

## Credits & License

© civilblur and MAZANOKE contributors. Source: https://github.com/civilblur/mazanoke

Changes by AIPMAndy. Licensed under [GNU GPL-3.0](https://github.com/civilblur/mazanoke/blob/main/LICENSE). More details in generated `dist/FORK-NOTICE.md` and `dist/docs/ATTRIBUTIONS.md`.