// Super JinX Panel. Copyright (c) 2026 Super JinX. See LICENSE.
// Run against an ORIGINAL source directory, never against generated output.
const fs=require('fs'),path=require('path');
const ob=require('javascript-obfuscator');
const [source,destination]=process.argv.slice(2);
if(!source||!destination)throw new Error('Usage: node obfuscate_web.cjs ORIGINAL_DIRECTORY OUTPUT_DIRECTORY');
const seed=Number(process.env.OBFUSCATION_SEED)||931472;
let state=seed>>>0;
function name(){let s='';for(let i=0;i<16;i++){state=(Math.imul(state,1664525)+1013904223)>>>0;s+='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'[(state>>>8)%52];}return s;}
const dictionary=Array.from({length:4096},name);
const opts={compact:true,controlFlowFlattening:true,controlFlowFlatteningThreshold:1,deadCodeInjection:true,deadCodeInjectionThreshold:.4,identifierNamesGenerator:'dictionary',identifiersDictionary:dictionary,renameGlobals:true,renameProperties:false,numbersToExpressions:true,simplify:true,splitStrings:true,splitStringsChunkLength:5,stringArray:true,stringArrayEncoding:['rc4'],stringArrayThreshold:1,stringArrayCallsTransform:true,stringArrayCallsTransformThreshold:1,stringArrayIndexShift:true,stringArrayRotate:true,stringArrayShuffle:true,stringArrayWrappersCount:3,stringArrayWrappersChainedCalls:true,stringArrayWrappersType:'function',transformObjectKeys:true,unicodeEscapeSequence:true,sourceMap:false,target:'browser',seed};
const credit='/* Super JinX Panel. Copyright (c) 2026 Super JinX. See LICENSE. */\n';
function transform(code,n){return credit+ob.obfuscate(code,{...opts,seed:seed+n}).getObfuscatedCode().replace(/<\/script/gi,'<\\/script');}
fs.mkdirSync(destination,{recursive:true});
fs.writeFileSync(path.join(destination,'jinx-ui.js'),transform(fs.readFileSync(path.join(source,'jinx-ui.js'),'utf8'),0)+'\n');
let html=fs.readFileSync(path.join(source,'sub.html'),'utf8');
const matches=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].filter(m=>!(/application\/json|\bsrc\s*=/.test(m[1])));
if(matches.length!==3||!matches[1][2].includes('root.JinxQR = api'))throw new Error('Unexpected subscription script layout');
const qr=matches[1][2].replace('root.JinxQR = api','JinxQR = api');
const joined='(function(){var JinxQR;\n'+qr+'\n'+matches[2][2]+'\n})();';
const replacements=[matches[0][0],'<script>'+transform(joined,1)+'</script>',''];
for(let i=matches.length-1;i>=0;i--){const m=matches[i];html=html.slice(0,m.index)+replacements[i]+html.slice(m.index+m[0].length);}
fs.writeFileSync(path.join(destination,'sub.html'),html);
console.log('Dashboard protected; QR and subscription code share a private scope.');
