#!/usr/bin/env python3
from pathlib import Path
import argparse, json, zipfile
from xml.sax.saxutils import escape, quoteattr

ROOT=Path(__file__).resolve().parents[1]
PKG=json.loads((ROOT/'package.json').read_text(encoding='utf-8'))
VERSION=PKG['version']
DEFAULT=ROOT/'dist'/f'agent-workflow-model-catalog-{VERSION}.vsix'

def q(value):
    return quoteattr(str(value))

def text(value):
    return escape(str(value))

def manifest_xml():
    engine=PKG['engines']['vscode']
    kinds=PKG.get('extensionKind') or []
    kind=','.join(kinds) if isinstance(kinds,list) else str(kinds)
    categories=','.join(PKG.get('categories') or ['Other'])
    executes='true' if PKG.get('main') or PKG.get('browser') else 'false'
    return f'''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id={q(PKG['name'])} Version={q(PKG['version'])} Publisher={q(PKG['publisher'])} />
    <DisplayName>{text(PKG.get('displayName',PKG['name']))}</DisplayName>
    <Description xml:space="preserve">{text(PKG.get('description',''))}</Description>
    <Tags>agent-workflow,language-model-tools</Tags>
    <Categories>{text(categories)}</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value={q(engine)} />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value={q(kind)} />
      <Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.PreRelease" Value="false" />
      <Property Id="Microsoft.VisualStudio.Code.ExecutesCode" Value={q(executes)} />
      <Property Id="Microsoft.VisualStudio.Services.GitHubFlavoredMarkdown" Value="true" />
      <Property Id="Microsoft.VisualStudio.Services.Content.Pricing" Value="Free" />
    </Properties>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" />
  </Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/readme.md" Addressable="true" />
  </Assets>
</PackageManifest>
'''

CONTENT_TYPES='''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="js" ContentType="application/javascript" />
  <Default Extension="md" ContentType="text/markdown" />
  <Default Extension="vsixmanifest" ContentType="text/xml" />
  <Override PartName="/extension.vsixmanifest" ContentType="text/xml" />
</Types>
'''

def zi(name):
    info=zipfile.ZipInfo(name,(1980,1,1,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o100644 << 16
    return info

def add_bytes(z,name,data):
    if isinstance(data,str):
        data=data.encode('utf-8')
    z.writestr(zi(name),data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def build(out):
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    required=[ROOT/'out'/'extension.js',ROOT/'out'/'catalog.js']
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit('Compile first; missing: '+', '.join(missing))
    with zipfile.ZipFile(out,'w') as z:
        add_bytes(z,'[Content_Types].xml',CONTENT_TYPES)
        add_bytes(z,'extension.vsixmanifest',manifest_xml())
        add_bytes(z,'extension/package.json',(ROOT/'package.json').read_bytes())
        add_bytes(z,'extension/readme.md',(ROOT/'README.md').read_bytes())
        for p in sorted((ROOT/'out').glob('*.js')):
            add_bytes(z,'extension/out/'+p.name,p.read_bytes())
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default=str(DEFAULT))
    args=ap.parse_args()
    print(build(args.out))
