/* FreePhoto static UI localization; upstream image engine is unchanged. */
(() => {
"use strict";
const translations=new Map(Object.entries({
"Drop or paste images":"拖入或粘贴图片",
"Browse":"浏览文件","Cancel":"取消","Settings":"设置","Images":"图片",
"Images are processed locally on your device, ensuring privacy.":"图片全部在本地处理，无需上传。",
"Optimization method":"优化方式",
"Set image quality":"调整图片质量","Limit file size":"限制文件大小",
"Try to compress the image to a target file size.":"尝试压缩到指定大小。",
"Quality":"画质","Target file size":"目标文件大小",
"Megabytes (MB)":"兆字节 (MB)","Kilobytes (KB)":"千字节 (KB)",
"Dimensions":"图片尺寸","Keep original dimensions":"保留原始尺寸",
"Do not alter the width and height of the image.":"不改变图片宽高。",
"Limit dimensions":"限制尺寸","Limit the width and height of the image.":"限制图片最大宽高。",
"Convert to":"转换为","Default":"默认",
"Optimized images ready for review and download.":"图片已处理完成，可预览和下载。",
"Delete all":"全部删除","Download all":"打包下载",
"No image optimized yet":"暂无处理结果",
"Upload images above to optimize them. Once compressed,":"添加图片后开始优化。",
"they'll appear here.":"处理结果将在这里显示。",
"Install MAZANOKE":"安装 FreePhoto",
"An app shortcut is added to your device.":"将应用添加到设备主屏幕。",
"Use even without an internet connection.":"安装后支持离线使用。",
"Install":"安装","Update available":"发现新版本",
"Refresh the page to update.":"刷新网页完成更新。",
"Ignore":"忽略","Refresh":"刷新"
}));
function translate(){
const walk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
let n;
while(n=walk.nextNode()){
const p=n.parentElement;
if(!p || ["SCRIPT","STYLE","TEXTAREA","CODE"].includes(p.tagName))continue;
const original=n.nodeValue.trim(), replacement=translations.get(original);
if(replacement && replacement!==original)n.nodeValue=n.nodeValue.replace(original,replacement);
}}
translate();
let scheduled=false;
new MutationObserver(()=>{if(scheduled)return;scheduled=true;queueMicrotask(()=>{scheduled=false;translate()})})
.observe(document.body,{subtree:true,childList:true,characterData:true});
})();
