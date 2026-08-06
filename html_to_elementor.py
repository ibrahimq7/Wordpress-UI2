#!/usr/bin/env python3
"""
HTML/CSS to Elementor Pro JSON Converter - Visual Tree Runtime Engine
Professional-grade compiler with headless browser geometry computation for 100% accuracy.

Master System Core Architecture:
1. HEADLESS VIEWPORT ENGINE (Playwright) - Mounts HTML into browser, computes exact pixel metrics
2. COMPILER MATRIX & TREE FLATTENER - Calculates percentages, flattens redundant depths <5
3. TOKENS HYDRATION PIPELINE - Injects Industrial Sophistication design tokens
4. PRODUCTION OUTPUT FORMAT - Native Elementor Pro JSON with safe escaping
"""

import json, uuid, hashlib, re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class DesignTokens:
    """Hardcoded Industrial Sophistication design token array."""
    FONT_HEADING = 'Geist'
    FONT_HEADING_WEIGHT = '600'
    FONT_BODY = 'Inter'
    FONT_BODY_WEIGHT = '400'
    CARD_BORDER_RADIUS = 16
    SHADOW_SOFT_LONG = '0 20px 40px rgba(10, 25, 47, 0.05)'
    
    @classmethod
    def apply_heading_typography(cls, settings):
        settings['typography_typography'] = 'custom'
        settings['typography_font_family'] = cls.FONT_HEADING
        settings['typography_font_weight'] = cls.FONT_HEADING_WEIGHT
    
    @classmethod
    def apply_body_typography(cls, settings):
        settings['typography_typography'] = 'custom'
        settings['typography_font_family'] = cls.FONT_BODY
        settings['typography_font_weight'] = cls.FONT_BODY_WEIGHT
    
    @classmethod
    def apply_card_styling(cls, settings):
        settings['border_radius'] = {'topLeft': cls.CARD_BORDER_RADIUS, 'topRight': cls.CARD_BORDER_RADIUS,
            'bottomLeft': cls.CARD_BORDER_RADIUS, 'bottomRight': cls.CARD_BORDER_RADIUS, 'unit': 'px', 'isLinked': True}
        settings['box_shadow_type'] = 'custom'
        settings['box_shadow'] = [{'horizontal': 0, 'vertical': 20, 'blur': 40, 'spread': 0, 'color': 'rgba(10, 25, 47, 0.05)'}]


@dataclass
class ComputedGeometry:
    width: float = 0.0; height: float = 0.0; x: float = 0.0; y: float = 0.0
    display: str = ''; flex_direction: str = ''; justify_content: str = ''; align_items: str = ''
    flex_wrap: str = ''; gap: float = 0.0; background_color: str = ''
    padding_top: float = 0.0; padding_right: float = 0.0; padding_bottom: float = 0.0; padding_left: float = 0.0
    margin_top: float = 0.0; margin_right: float = 0.0; margin_bottom: float = 0.0; margin_left: float = 0.0
    border_top_left_radius: float = 0.0; border_top_right_radius: float = 0.0
    border_bottom_left_radius: float = 0.0; border_bottom_right_radius: float = 0.0
    font_family: str = ''; font_size: float = 0.0; font_weight: str = ''; color: str = ''
    text_align: str = ''; line_height: str = ''; letter_spacing: str = ''
    position: str = ''; top: float = 0.0; left: float = 0.0; z_index: str = ''
    opacity: float = 1.0; visibility: str = 'visible'; overflow: str = ''
    min_width: str = ''; max_width: str = ''; min_height: str = ''; max_height: str = ''
    tag_name: str = ''; id: str = ''; class_name: str = ''; text_content: str = ''
    inner_html: str = ''; src: str = ''; href: str = ''; alt: str = ''
    placeholder: str = ''; value: str = ''; element_type: str = ''; name_attr: str = ''


class HeadlessViewportEngine:
    """COMPUTED GEOMETRY ENGINE: Uses Playwright to extract exact computed styles."""
    JS_CODE = """() => {
        function pf(v){if(!v||v==='auto'||v==='normal')return 0;const n=parseFloat(v);return isNaN(n)?0:n;}
        const r=[];const w=document.createTreeWalker(document.body||document.documentElement,NodeFilter.SHOW_ELEMENT);
        let n;while(n=w.nextNode()){if(['SCRIPT','STYLE','META','LINK','HEAD','BR','HR'].includes(n.tagName))continue;
        const c=getComputedStyle(n),b=n.getBoundingClientRect();if(c.visibility==='hidden'||c.display==='none'||(b.width===0&&b.height===0&&!n.children.length))continue;
        r.push({tagName:n.tagName.toLowerCase(),id:n.id||'',className:n.className||'',textContent:n.textContent?n.textContent.trim().slice(0,5000):'',innerHTML:n.innerHTML?n.innerHTML.slice(0,10000):'',width:b.width,height:b.height,x:b.x,y:b.y,top:b.top,left:b.left,right:b.right,bottom:b.bottom,display:c.display,position:c.position,flexDirection:c.flexDirection,flexWrap:c.flexWrap,justifyContent:c.justifyContent,alignItems:c.alignItems,gap:pf(c.gap),paddingTop:pf(c.paddingTop),paddingRight:pf(c.paddingRight),paddingBottom:pf(c.paddingBottom),paddingLeft:pf(c.paddingLeft),marginTop:pf(c.marginTop),marginRight:pf(c.marginRight),marginBottom:pf(c.marginBottom),marginLeft:pf(c.marginLeft),borderTopLeftRadius:pf(c.borderTopLeftRadius),borderTopRightRadius:pf(c.borderTopRightRadius),borderBottomLeftRadius:pf(c.borderBottomLeftRadius),borderBottomRightRadius:pf(c.borderBottomRightRadius),backgroundColor:c.backgroundColor,fontFamily:c.fontFamily,fontSize:pf(c.fontSize),fontWeight:c.fontWeight,color:c.color,textAlign:c.textAlign,lineHeight:c.lineHeight,opacity:pf(c.opacity),overflow:c.overflow,minWidth:c.minWidth,maxWidth:c.maxWidth,minHeight:c.minHeight,maxHeight:c.maxHeight,src:n.getAttribute('src')||'',href:n.getAttribute('href')||'',alt:n.getAttribute('alt')||'',placeholder:n.getAttribute('placeholder')||'',value:n.value||'',type:n.getAttribute('type')||'',name:n.getAttribute('name')||''});}
        return r;}"""
    
    def __init__(self, vw=1920, vh=1080):
        self.vw, self.vh, self.pw, self.br, self.pg = vw, vh, None, None, None
    def __enter__(self):
        if not PLAYWRIGHT_AVAILABLE: raise RuntimeError("Playwright not installed")
        self.pw = sync_playwright().start()
        self.br = self.pw.chromium.launch(headless=True)
        self.pg = self.br.new_page(viewport={'width': self.vw, 'height': self.vh})
        return self
    def __exit__(self, *a):
        if self.br: self.br.close()
        if self.pw: self.pw.stop()
    def load_html(self, html, css=""):
        if css:
            if '<head>' in html and '</head>' in html: html = html.replace('</head>', f'<style>{css}</style></head>')
            elif '<body>' in html: html = html.replace('<body>', f'<body><style>{css}</style>')
            else: html = f'<style>{css}</style>{html}'
        self.pg.goto(f'data:text/html;charset=utf-8,{html}', wait_until='networkidle')
        self.pg.wait_for_load_state('domcontentloaded'); self.pg.wait_for_timeout(500)
        return self.pg.evaluate(self.JS_CODE)
    def parent_map(self, data):
        pm = {}; si = sorted(range(len(data)), key=lambda i: data[i]['width']*data[i]['height'])
        for i in si:
            e, er = data[i], (data[i]['left'], data[i]['top'], data[i]['right'], data[i]['bottom'])
            pi, ma = None, float('inf')
            for j in range(len(data)):
                if i == j: continue
                o = data[j]; otr = (o['left'], o['top'], o['right'], o['bottom'])
                if otr[0]<=er[0] and otr[1]<=er[1] and otr[2]>=er[2] and otr[3]>=er[3]:
                    a = o['width']*o['height']
                    if 0<a<ma: ma, pi = a, j
            pm[i] = pi
        return pm


class CSSParser:
    @staticmethod
    def parse_inline(s):
        if not s: return {}
        return {k.strip().lower(): v.strip() for p in s.split(';') if ':' in p for k, v in [p.split(':', 1)]}
    @staticmethod
    def parse_file(css):
        st = {}; css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        for sel, rules in re.findall(r'([^@{}]+)\{([^{}]+)\}', css):
            sel = sel.strip()
            if sel.startswith('@') or sel == ':root': continue
            props = {k.strip().lower(): v.strip() for k, v in re.findall(r'([\w-]+)\s*:\s*([^;]+);?', rules)}
            if props: st[sel] = props
        return st


class TreeFlattener:
    MAX_DEPTH = 4
    @classmethod
    def skip_wrapper(cls, g, cc):
        if g.display in ('flex', 'grid', 'inline-flex', 'inline-grid'): return False
        return cc <= 1 and not cls._has_styles(g)
    @classmethod
    def _has_styles(cls, g):
        if g.background_color and g.background_color != 'transparent': return True
        if any([g.padding_top, g.padding_right, g.padding_bottom, g.padding_left]): return True
        if any([g.border_top_left_radius, g.border_top_right_radius, g.border_bottom_left_radius, g.border_bottom_right_radius]): return True
        return bool(g.min_width or g.max_width or g.min_height or g.max_height)


class LayoutCompiler:
    JM = {'flex-start':'flex-start','start':'flex-start','center':'center','flex-end':'flex-end','end':'flex-end','space-between':'space-between','space-around':'space-around','space-evenly':'space-evenly'}
    AM = {'flex-start':'flex-start','start':'flex-start','center':'center','flex-end':'flex-end','end':'flex-end','stretch':'stretch','baseline':'baseline'}
    DM = {'row':'row','row-reverse':'row-reverse','column':'column','column-reverse':'column-reverse'}
    WM = {'nowrap':'nowrap','wrap':'wrap','wrap-reverse':'wrap-reverse'}
    
    @classmethod
    def container_settings(cls, g, pw=0.0):
        s = {'content_width':'boxed','flex_direction':'column','flex_wrap':'nowrap','justify_content':'center','align_items':'center'}
        if g.flex_direction: s['flex_direction'] = cls.DM.get(g.flex_direction, 'column')
        elif g.display in ('flex', 'inline-flex'): s['flex_direction'] = 'row'
        if g.flex_wrap: s['flex_wrap'] = cls.WM.get(g.flex_wrap, 'nowrap')
        if g.justify_content: s['justify_content'] = cls.JM.get(g.justify_content, 'center')
        if g.align_items: s['align_items'] = cls.AM.get(g.align_items, 'center')
        if g.gap > 0: s['gap'] = {'column': g.gap, 'row': g.gap}
        if any([g.padding_top, g.padding_right, g.padding_bottom, g.padding_left]):
            s['padding'] = {'top': g.padding_top, 'right': g.padding_right, 'bottom': g.padding_bottom, 'left': g.padding_left, 'unit': 'px', 'isLinked': False}
        if any([g.margin_top, g.margin_right, g.margin_bottom, g.margin_left]):
            s['margin'] = {'top': g.margin_top, 'right': g.margin_right, 'bottom': g.margin_bottom, 'left': g.margin_left, 'unit': 'px', 'isLinked': False}
        if g.background_color and g.background_color != 'transparent':
            s['background_background'] = 'classic'; s['background_color'] = g.background_color
        if pw > 0 and g.width > 0: s['width'] = {'unit': '%', 'size': round((g.width/pw)*100, 2), 'sizes': []}
        elif g.width > 0: s['width'] = {'unit': 'px', 'size': g.width, 'sizes': []}
        ar = (g.border_top_left_radius + g.border_top_right_radius + g.border_bottom_left_radius + g.border_bottom_right_radius) / 4
        if ar > 0: s['border_radius'] = {'topLeft': ar, 'topRight': ar, 'bottomLeft': ar, 'bottomRight': ar, 'unit': 'px', 'isLinked': True}
        return s
    
    @classmethod
    def widget_settings(cls, g, wt):
        s = {}
        if wt == 'heading': DesignTokens.apply_heading_typography(s)
        elif wt in ('text-editor', 'button'): DesignTokens.apply_body_typography(s)
        if g.color and g.color != 'transparent':
            if wt == 'heading': s['title_color'] = g.color
            elif wt == 'text-editor': s['text_color'] = g.color
            elif wt == 'button': s['button_text_color'] = g.color
        if g.font_size > 0: s['typography_font_size'] = {'unit': 'px', 'size': g.font_size, 'sizes': []}
        if g.font_weight:
            try: s['typography_font_weight'] = str(int(g.font_weight))
            except: s['typography_font_weight'] = {'normal':'400','regular':'400','bold':'700','light':'300','medium':'500','semibold':'600'}.get(g.font_weight.lower(), '400')
        if g.text_align: s['horizontal_align'] = g.text_align
        if wt == 'button':
            if g.background_color and g.background_color != 'transparent':
                s['button_background_color'] = g.background_color; s['background_background'] = 'classic'; s['background_color'] = g.background_color
            DesignTokens.apply_card_styling(s)
        return s
    
    @classmethod
    def widget_type(cls, tag):
        m = {'h1':'heading','h2':'heading','h3':'heading','h4':'heading','h5':'heading','h6':'heading','p':'text-editor','span':'text-editor','div':'container','section':'container','article':'container','header':'container','footer':'container','nav':'container','main':'container','aside':'container','ul':'icon-list','ol':'icon-list','li':'text-editor','a':'button','button':'button','img':'image','svg':'html','input':'form','textarea':'form'}
        return m.get(tag.lower(), 'text-editor')
    
    @classmethod
    def is_container(cls, tag):
        return tag.lower() in {'div','section','article','header','footer','nav','main','aside','ul','ol','form'}


class IdGen:
    def __init__(self, seed=None):
        self.seed = seed or str(uuid.uuid4()); self.c = 0
    def gen(self, n=""):
        self.c += 1
        return hashlib.md5(f"{self.seed}_{n}_{self.c}".encode()).hexdigest()[:7]


class VisualTreeRuntimeEngine:
    def __init__(self, title="Converted Template", vw=1920, vh=1080):
        self.title, self.vw, self.vh, self.id_gen = title, vw, vh, IdGen()
    
    def convert(self, html, css="", title=None):
        if title: self.title = title
        if Path(html).exists():
            with open(html, 'r', encoding='utf-8') as f: html = f.read()
        if css and Path(css).exists():
            with open(css, 'r', encoding='utf-8') as f: css = f.read()
        
        geoms = []
        if PLAYWRIGHT_AVAILABLE:
            try:
                with HeadlessViewportEngine(self.vw, self.vh) as eng:
                    data = eng.load_html(html, css)
                    pm = eng.parent_map(data)
                    for d in data:
                        g = ComputedGeometry(width=d.get('width',0),height=d.get('height',0),x=d.get('x',0),y=d.get('y',0),display=d.get('display',''),flex_direction=d.get('flexDirection',''),justify_content=d.get('justifyContent',''),align_items=d.get('alignItems',''),flex_wrap=d.get('flexWrap',''),gap=d.get('gap',0),background_color=d.get('backgroundColor',''),padding_top=d.get('paddingTop',0),padding_right=d.get('paddingRight',0),padding_bottom=d.get('paddingBottom',0),padding_left=d.get('paddingLeft',0),margin_top=d.get('marginTop',0),margin_right=d.get('marginRight',0),margin_bottom=d.get('marginBottom',0),margin_left=d.get('marginLeft',0),border_top_left_radius=d.get('borderTopLeftRadius',0),border_top_right_radius=d.get('borderTopRightRadius',0),border_bottom_left_radius=d.get('borderBottomLeftRadius',0),border_bottom_right_radius=d.get('borderBottomRightRadius',0),font_family=d.get('fontFamily',''),font_size=d.get('fontSize',0),font_weight=d.get('fontWeight',''),color=d.get('color',''),text_align=d.get('textAlign',''),line_height=d.get('lineHeight',''),letter_spacing=d.get('letterSpacing',''),position=d.get('position',''),top=d.get('top',0),left=d.get('left',0),z_index=d.get('zIndex',''),opacity=d.get('opacity',1.0),visibility=d.get('visibility','visible'),overflow=d.get('overflow',''),min_width=d.get('minWidth',''),max_width=d.get('maxWidth',''),min_height=d.get('minHeight',''),max_height=d.get('maxHeight',''))
                        g.tag_name, g.id, g.class_name = d.get('tagName',''), d.get('id',''), d.get('className','')
                        g.text_content, g.inner_html = d.get('textContent',''), d.get('innerHTML','')
                        g.src, g.href, g.alt = d.get('src',''), d.get('href',''), d.get('alt','')
                        g.placeholder, g.value = d.get('placeholder',''), d.get('value','')
                        g.element_type, g.name_attr = d.get('type',''), d.get('name','')
                        geoms.append(g)
                    em = {i: {'geometry': g, 'children': [], 'index': i} for i, g in enumerate(geoms)}
                    for ci, pi in pm.items():
                        if pi is not None and pi in em: em[pi]['children'].append(em[ci])
                    roots = [e for i, e in em.items() if pm.get(i) is None]
            except Exception as ex:
                print(f"Playwright failed: {ex}")
                geoms = self._bs4_parse(html, css)
                roots = self._bs4_tree(geoms)
        else:
            geoms = self._bs4_parse(html, css)
            roots = self._bs4_tree(geoms)
        
        content = []
        for r in roots:
            cn = self._compile(r, geoms, self.vw, 0)
            if cn:
                if cn.get('_lift'): content.extend(cn.get('elements', []))
                elif cn.get('elType') == 'container': content.append(cn)
                else: content.append({'id': self.id_gen.gen('wrapper'), 'elType': 'container', 'settings': {'flex_direction': 'column', 'content_width': 'boxed'}, 'elements': [cn]})
        
        return json.dumps({'version': '0.4', 'title': self.title, 'type': 'page', 'content': content, 'page_settings': {'post_status': 'publish'}}, indent=2, ensure_ascii=False)
    
    def _bs4_parse(self, html, css):
        if not BS4_AVAILABLE: raise ImportError("pip install beautifulsoup4")
        soup = BeautifulSoup(html, 'html.parser')
        rules = CSSParser.parse_file(css) if css else {}
        geoms = []
        for e in soup.find_all(True):
            if e.name in ('script','style','meta','link','head','br','hr'): continue
            st = {}
            if e.get('style'): st.update(CSSParser.parse_inline(e.get('style')))
            cls = e.get('class', [])
            if isinstance(cls, str): cls = cls.split()
            for c in cls:
                if f'.{c}' in rules: st.update(rules[f'.{c}'])
            g = ComputedGeometry(tag_name=e.name, id=e.get('id',''), class_name=' '.join(cls) if cls else '', text_content=e.get_text(strip=True), inner_html=str(e.contents) if e.contents else '', src=e.get('src',''), href=e.get('href',''), alt=e.get('alt',''), placeholder=e.get('placeholder',''), value=e.get('value',''), element_type=e.get('type',''), name_attr=e.get('name',''))
            if 'display' in st: g.display = st['display']
            if 'flex-direction' in st: g.flex_direction = st['flex-direction']
            if 'justify-content' in st: g.justify_content = st['justify-content']
            if 'align-items' in st: g.align_items = st['align-items']
            if 'flex-wrap' in st: g.flex_wrap = st['flex-wrap']
            if 'background-color' in st: g.background_color = st['background-color']
            if 'color' in st: g.color = st['color']
            if 'font-family' in st: g.font_family = st['font-family'].split(',')[0].strip().strip('"\'')
            if 'font-size' in st:
                m = re.match(r'([\d.]+)', st['font-size'])
                if m: g.font_size = float(m.group(1))
            if 'font-weight' in st: g.font_weight = st['font-weight']
            if 'text-align' in st: g.text_align = st['text-align']
            for d in ['width','height','min-width','max-width','min-height','max-height']:
                if d in st:
                    m = re.match(r'([\d.]+)', st[d])
                    if m: setattr(g, d.replace('-','_'), float(m.group(1)))
            for s in ['top','right','bottom','left']:
                for p in ['padding','margin']:
                    k = f'{p}-{s}'
                    if k in st:
                        m = re.match(r'([\d.]+)', st[k])
                        if m: setattr(g, f'{p}_{s}', float(m.group(1)))
            for c in ['top-left','top-right','bottom-left','bottom-right']:
                k = f'border-{c}-radius'
                if k in st:
                    m = re.match(r'([\d.]+)', st[k])
                    if m: setattr(g, f'border_{c.replace("-","_")}_radius', float(m.group(1)))
            geoms.append(g)
        return geoms
    
    def _bs4_tree(self, geoms):
        if not geoms: return []
        em = {i: {'geometry': g, 'children': [], 'index': i} for i, g in enumerate(geoms)}
        stack = []
        for i, ed in em.items():
            g = ed['geometry']
            while stack and not LayoutCompiler.is_container(stack[-1]['geometry'].tag_name): stack.pop()
            if stack: stack[-1]['children'].append(ed)
            if LayoutCompiler.is_container(g.tag_name): stack.append(ed)
        ac = set()
        for e in em.values():
            for c in e['children']: ac.add(c['index'])
        roots = [e for i, e in em.items() if i not in ac]
        return roots if roots else list(em.values())[:1]
    
    def _compile(self, ed, all_g, pw, depth):
        g, ch, tn = ed['geometry'], ed['children'], ed['geometry'].tag_name
        if tn == 'span' and not ch and not g.text_content.strip(): return None
        ic = LayoutCompiler.is_container(tn)
        if g.display in ('flex','grid','inline-flex','inline-grid') or len(ch) > 1: ic = True
        if not ic and tn == 'div':
            if TreeFlattener.skip_wrapper(g, len(ch)):
                lifted = []
                for c in ch:
                    cc = self._compile(c, all_g, pw, depth+1)
                    if cc:
                        if cc.get('_lift'): lifted.extend(cc.get('elements',[]))
                        else: lifted.append(cc)
                return {'_lift': True, 'elements': lifted} if lifted else None
        if ic: return self._comp_cont(ed, all_g, pw, depth)
        return self._comp_wid(ed)
    
    def _comp_cont(self, ed, all_g, pw, depth):
        g, ch = ed['geometry'], ed['children']
        s = LayoutCompiler.container_settings(g, pw)
        if g.border_top_left_radius >= DesignTokens.CARD_BORDER_RADIUS or g.border_top_right_radius >= DesignTokens.CARD_BORDER_RADIUS:
            DesignTokens.apply_card_styling(s)
        node = {'id': self.id_gen.gen(g.tag_name), 'elType': 'container', 'settings': s, 'elements': []}
        if g.class_name: node['settings']['css_classes'] = g.class_name
        if g.id: node['settings']['css_id'] = g.id
        for c in ch:
            cc = self._compile(c, all_g, g.width, depth+1)
            if cc:
                if cc.get('_lift'): node['elements'].extend(cc.get('elements',[]))
                else: node['elements'].append(cc)
        if depth >= TreeFlattener.MAX_DEPTH and node['elements']:
            fl = []
            for cn in node['elements']:
                if cn.get('elType') == 'container' and 'elements' in cn: fl.extend(cn['elements'])
                else: fl.append(cn)
            node['elements'] = fl
        return node
    
    def _comp_wid(self, ed):
        g, tn = ed['geometry'], ed['geometry'].tag_name
        wt = LayoutCompiler.widget_type(tn)
        s = {}
        if wt == 'heading':
            s['title'] = g.text_content or g.inner_html; s['header_size'] = tn
            DesignTokens.apply_heading_typography(s)
        elif wt == 'text-editor':
            s['editor'] = g.text_content or g.inner_html
            DesignTokens.apply_body_typography(s)
        elif wt == 'image':
            if g.src: s['image'] = {'url': g.src, 'alt': g.alt}
            else: return None
        elif wt == 'button':
            s['text'] = g.text_content or 'Button'
            s['link'] = {'url': g.href or '#', 'is_external': g.href.startswith('http') if g.href else False}
            DesignTokens.apply_body_typography(s)
        elif wt == 'icon-list': s['icon_list'] = []
        elif wt == 'html': s['html'] = g.inner_html
        elif wt == 'form':
            s['field_type'] = g.element_type or tn
            if g.name_attr: s['field_label'] = g.name_attr
        s.update(LayoutCompiler.widget_settings(g, wt))
        return {'id': self.id_gen.gen(tn), 'elType': 'widget', 'widgetType': wt, 'settings': s}
    
    def convert_files(self, hp, cp=None, op=None):
        with open(hp, 'r', encoding='utf-8') as f: hc = f.read()
        cc = ""
        if cp and Path(cp).exists():
            with open(cp, 'r', encoding='utf-8') as f: cc = f.read()
        elif Path(hp).with_suffix('.css').exists():
            with open(Path(hp).with_suffix('.css'), 'r', encoding='utf-8') as f: cc = f.read()
        t = Path(hp).stem.replace('-', ' ').replace('_', ' ').title()
        jo = self.convert(hc, cc, t)
        out = op or str(Path(hp).with_suffix('.elementor.json'))
        with open(out, 'w', encoding='utf-8') as f: f.write(jo)
        return jo


def main():
    import sys
    if len(sys.argv) < 2:
        print("HTML/CSS to Elementor Pro JSON Converter - Visual Tree Runtime Engine")
        print("Usage: python html_to_elementor.py <html_file> [css_file] [output_file]")
        sys.exit(1)
    hf = sys.argv[1]
    cf = sys.argv[2] if len(sys.argv) > 2 else None
    of = sys.argv[3] if len(sys.argv) > 3 else None
    eng = VisualTreeRuntimeEngine()
    try:
        jo = eng.convert_files(hf, cf, of)
        op = of or Path(hf).with_suffix('.elementor.json')
        print(f"Successfully converted to Elementor JSON\n  Output: {op}\n  Size: {len(jo)} bytes")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}"); sys.exit(1)
    except Exception as e:
        print(f"Error: {e}"); import traceback; traceback.print_exc(); sys.exit(1)

if __name__ == "__main__":
    main()
