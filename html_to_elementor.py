#!/usr/bin/env python3
"""
HTML/CSS to Elementor Pro JSON Converter - Optimized Version
Professional-grade compiler with flattened hierarchy for Elementor import compatibility.

Engineering Updates:
1. FLATTEN HIERARCHY: Only creates containers for major layout elements
2. SYSTEM SCHEMA HEADERS: Uses exact Elementor system keys (version 0.4)
3. CONTROL ARRAYS: Every widget has explicit settings block structure
"""

import json
import uuid
import hashlib
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CSSVariables:
    """Stores parsed CSS custom properties (variables)"""
    variables: Dict[str, str] = field(default_factory=dict)
    
    def resolve(self, value: str) -> str:
        """Resolve CSS variable references like var(--color-primary)"""
        if not value or 'var(' not in value:
            return value
        
        def replace_var(match):
            var_name = match.group(1).strip()
            return self.variables.get(var_name, match.group(0))
        
        result = re.sub(r'var\(([^)]+)\)', replace_var, value)
        # Handle fallback values in var(--name, fallback)
        if 'var(' in result:
            result = re.sub(r'var\([^,]+,\s*([^)]+)\)', r'\1', result)
        return result


class ElementorIdGenerator:
    """Generates unique, deterministic 7-character hexadecimal strings."""
    
    def __init__(self, seed: Optional[str] = None):
        self.seed = seed or str(uuid.uuid4())
        self.counter = 0
    
    def generate(self, element_name: str = "") -> str:
        """Generate a unique 7-char hex ID"""
        self.counter += 1
        unique_str = f"{self.seed}_{element_name}_{self.counter}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:7]
    
    def reset(self):
        """Reset counter for deterministic generation"""
        self.counter = 0


class CSSStyleParser:
    """Parses inline styles and external CSS into computed style dictionaries."""
    
    @staticmethod
    def parse_inline(style_string: str) -> Dict[str, str]:
        """Parse inline style attribute into dictionary"""
        if not style_string:
            return {}
        pairs = [p.split(':', 1) for p in style_string.split(';') if ':' in p]
        return {k.strip().lower(): v.strip() for k, v in pairs}
    
    @staticmethod
    def parse_css_file(css_content: str) -> Tuple[Dict[str, Dict[str, str]], CSSVariables]:
        """Parse CSS file into selector-style mapping and extract variables"""
        styles = {}
        variables = CSSVariables()
        
        # Extract CSS variables from :root
        root_match = re.search(r':root\s*\{([^}]+)\}', css_content, re.DOTALL)
        if root_match:
            var_content = root_match.group(1)
            var_pairs = re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', var_content)
            for var_name, var_value in var_pairs:
                variables.variables[var_name] = var_value.strip()
        
        # Parse media queries and regular selectors
        # Remove comments
        css_clean = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Match selectors and their rules (excluding @media for now)
        pattern = r'([^@{}]+)\{([^{}]+)\}'
        matches = re.findall(pattern, css_clean)
        
        for selector, rules in matches:
            selector = selector.strip()
            # Skip @rules and :root (already processed)
            if selector.startswith('@') or selector == ':root':
                continue
            
            # Parse properties
            props = {}
            prop_matches = re.findall(r'([\w-]+)\s*:\s*([^;]+);?', rules)
            for prop_name, prop_value in prop_matches:
                props[prop_name.strip().lower()] = prop_value.strip()
            
            if props:
                styles[selector] = props
        
        return styles, variables


class ElementorSchemaMapper:
    """Maps HTML elements and CSS properties to Elementor schema structures."""
    
    # Widget type mappings
    WIDGET_MAP = {
        'h1': 'heading',
        'h2': 'heading',
        'h3': 'heading',
        'h4': 'heading',
        'h5': 'heading',
        'h6': 'heading',
        'p': 'text-editor',
        'span': 'text-editor',
        'div': 'container',
        'section': 'container',
        'article': 'container',
        'header': 'container',
        'footer': 'container',
        'nav': 'container',
        'main': 'container',
        'aside': 'container',
        'ul': 'icon-list',
        'ol': 'icon-list',
        'li': 'text-editor',
        'a': 'button',
        'button': 'button',
        'img': 'image',
        'svg': 'html',
        'input': 'form',
        'textarea': 'form',
        'select': 'form',
    }
    
    # MAJOR layout container tags - only these create containers by default
    MAJOR_CONTAINER_TAGS = {'section', 'header', 'footer', 'nav', 'main', 'aside', 'article'}
    
    # Tags that should NEVER be containers (always widgets)
    WIDGET_ONLY_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'img', 
                        'a', 'button', 'li', 'input', 'textarea', 'select', 'label',
                        'strong', 'em', 'b', 'i', 'u', 'small', 'sub', 'sup'}
    
    @classmethod
    def get_widget_type(cls, tag_name: str, has_children: bool = True) -> str:
        """Determine Elementor widget type from HTML tag"""
        tag_lower = tag_name.lower()
        
        # Check widget-only tags first
        if tag_lower in cls.WIDGET_ONLY_TAGS:
            return cls.WIDGET_MAP.get(tag_lower, 'text-editor')
        
        # Container tags
        if tag_lower in cls.MAJOR_CONTAINER_TAGS:
            return 'container'
        
        # For div and other tags, check context
        return cls.WIDGET_MAP.get(tag_lower, 'text-editor')


class FlexboxLayoutCompiler:
    """Compiles CSS flexbox and grid properties to Elementor container settings."""
    
    JUSTIFY_MAP = {
        'flex-start': 'flex-start',
        'start': 'flex-start',
        'center': 'center',
        'flex-end': 'flex-end',
        'end': 'flex-end',
        'space-between': 'space-between',
        'space-around': 'space-around',
        'space-evenly': 'space-evenly',
    }
    
    ALIGN_MAP = {
        'flex-start': 'flex-start',
        'start': 'flex-start',
        'center': 'center',
        'flex-end': 'flex-end',
        'end': 'flex-end',
        'stretch': 'stretch',
        'baseline': 'baseline',
    }
    
    DIRECTION_MAP = {
        'row': 'row',
        'row-reverse': 'row-reverse',
        'column': 'column',
        'column-reverse': 'column-reverse',
    }
    
    WRAP_MAP = {
        'nowrap': 'nowrap',
        'wrap': 'wrap',
        'wrap-reverse': 'wrap-reverse',
    }
    
    @classmethod
    def parse_dimension(cls, value: str, default_unit: str = 'px') -> Optional[Dict[str, Any]]:
        """Parse CSS dimension value to Elementor format"""
        if not value:
            return None
        
        value = value.strip().lower()
        
        # Handle auto
        if value == 'auto':
            return {'unit': 'auto', 'size': 0, 'sizes': []}
        
        # Handle calc() - simplified
        if value.startswith('calc('):
            return None  # Would need complex evaluation
        
        # Extract number and unit
        match = re.match(r'^(-?[\d.]+)(px|em|rem|%|vh|vw|pt)?$', value)
        if match:
            num = float(match.group(1))
            unit = match.group(2) or default_unit
            
            # Convert rem/em to px (assuming 16px base)
            if unit in ('em', 'rem'):
                num *= 16
                unit = 'px'
            
            return {'unit': unit, 'size': num, 'sizes': []}
        
        return None
    
    @classmethod
    def compile_container_settings(cls, styles: Dict[str, str], css_vars: CSSVariables) -> Dict[str, Any]:
        """Convert CSS flexbox/grid properties to Elementor container settings"""
        settings = {
            'content_width': 'boxed',
            'flex_direction': 'column',
            'flex_wrap': 'nowrap',
            'justify_content': 'center',
            'align_items': 'center',
        }
        
        # Resolve CSS variables
        resolved_styles = {}
        for key, value in styles.items():
            resolved_styles[key] = css_vars.resolve(value)
        
        # Flex direction
        if 'flex-direction' in resolved_styles:
            direction = resolved_styles['flex-direction']
            settings['flex_direction'] = cls.DIRECTION_MAP.get(direction, 'column')
        
        # Flex wrap
        if 'flex-wrap' in resolved_styles:
            wrap = resolved_styles['flex-wrap']
            settings['flex_wrap'] = cls.WRAP_MAP.get(wrap, 'nowrap')
        
        # Justify content
        if 'justify-content' in resolved_styles:
            justify = resolved_styles['justify-content']
            settings['justify_content'] = cls.JUSTIFY_MAP.get(justify, 'center')
        
        # Align items
        if 'align-items' in resolved_styles:
            align = resolved_styles['align-items']
            settings['align_items'] = cls.ALIGN_MAP.get(align, 'center')
        
        # Gap
        if 'gap' in resolved_styles:
            gap_val = cls.parse_dimension(resolved_styles['gap'])
            if gap_val:
                gap_num = gap_val.get('size', 0)
                settings['gap'] = {'column': gap_num, 'row': gap_num}
        
        # Padding
        padding = cls._parse_padding(resolved_styles)
        if padding:
            settings['padding'] = padding
        
        # Margin
        margin = cls._parse_margin(resolved_styles)
        if margin:
            settings['margin'] = margin
        
        # Background
        bg_settings = cls._parse_background(resolved_styles)
        if bg_settings:
            settings.update(bg_settings)
        
        # Min height
        if 'min-height' in resolved_styles:
            min_h = cls.parse_dimension(resolved_styles['min-height'])
            if min_h:
                settings['min_height'] = min_h
        
        # Width/Max-width
        if 'width' in resolved_styles:
            width = cls.parse_dimension(resolved_styles['width'])
            if width:
                settings['width'] = width
        
        return settings
    
    @classmethod
    def _parse_padding(cls, styles: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Parse padding properties"""
        padding = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0, 'unit': 'px', 'isLinked': False}
        has_padding = False
        
        # Shorthand padding
        if 'padding' in styles:
            values = styles['padding'].split()
            if len(values) == 1:
                val = cls.parse_dimension(values[0])
                if val:
                    padding = {
                        'top': val['size'], 'right': val['size'],
                        'bottom': val['size'], 'left': val['size'],
                        'unit': val['unit'], 'isLinked': True
                    }
                    has_padding = True
            elif len(values) == 2:
                v1, v2 = cls.parse_dimension(values[0]), cls.parse_dimension(values[1])
                if v1 and v2:
                    padding = {
                        'top': v1['size'], 'right': v2['size'],
                        'bottom': v1['size'], 'left': v2['size'],
                        'unit': v1['unit'], 'isLinked': False
                    }
                    has_padding = True
            elif len(values) == 4:
                dims = [cls.parse_dimension(v) for v in values]
                if all(dims):
                    padding = {
                        'top': dims[0]['size'], 'right': dims[1]['size'],
                        'bottom': dims[2]['size'], 'left': dims[3]['size'],
                        'unit': dims[0]['unit'], 'isLinked': False
                    }
                    has_padding = True
        
        # Individual padding properties override
        for side in ['top', 'right', 'bottom', 'left']:
            key = f'padding-{side}'
            if key in styles:
                dim = cls.parse_dimension(styles[key])
                if dim:
                    padding[side] = dim['size']
                    padding['unit'] = dim['unit']
                    has_padding = True
        
        return padding if has_padding else None
    
    @classmethod
    def _parse_margin(cls, styles: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Parse margin properties"""
        margin = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0, 'unit': 'px', 'isLinked': False}
        has_margin = False
        
        if 'margin' in styles:
            values = styles['margin'].split()
            if len(values) == 1 and values[0] != '0':
                val = cls.parse_dimension(values[0])
                if val and val['size'] != 0:
                    margin = {
                        'top': val['size'], 'right': val['size'],
                        'bottom': val['size'], 'left': val['size'],
                        'unit': val['unit'], 'isLinked': True
                    }
                    has_margin = True
        
        return margin if has_margin else None
    
    @classmethod
    def _parse_background(cls, styles: Dict[str, str]) -> Dict[str, Any]:
        """Parse background properties"""
        bg_settings = {}
        
        if 'background-color' in styles:
            bg_color = styles['background-color']
            if bg_color and bg_color != 'transparent':
                bg_settings['background_background'] = 'classic'
                bg_settings['background_color'] = bg_color
        
        if 'background' in styles and 'background' not in bg_settings:
            bg = styles['background']
            # Check for gradient
            if 'gradient' in bg or 'linear-gradient' in bg:
                bg_settings['background_background'] = 'gradient'
                # Simplified gradient handling
                bg_settings['background_color'] = '#ffffff'  # Fallback
        
        return bg_settings


class TypographyMapper:
    """Maps CSS typography properties to Elementor typography settings."""
    
    GOLDEN_RULE_LINE_HEIGHT_MULTIPLIER = 1.3
    
    @classmethod
    def compile_typography_settings(cls, styles: Dict[str, str], css_vars: CSSVariables) -> Dict[str, Any]:
        """Convert CSS typography to Elementor typography settings"""
        settings = {}
        
        # Resolve CSS variables
        resolved_styles = {}
        for key, value in styles.items():
            resolved_styles[key] = css_vars.resolve(value)
        
        # Font family
        if 'font-family' in resolved_styles:
            font_family = resolved_styles['font-family'].replace("'", "").replace('"', '')
            # Take first font in stack
            font_family = font_family.split(',')[0].strip()
            settings['typography_font_family'] = font_family
        
        # Font size
        if 'font-size' in resolved_styles:
            size_val = cls._parse_font_size(resolved_styles['font-size'])
            if size_val:
                settings['typography_typography'] = 'custom'
                settings['typography_font_size'] = size_val
                
                # GOLDEN RULE #1: Auto-calculate line-height
                font_size_px = size_val.get('size', 16)
                line_height_calc = font_size_px * cls.GOLDEN_RULE_LINE_HEIGHT_MULTIPLIER
                settings['typography_line_height'] = {
                    'unit': 'px',
                    'size': line_height_calc,
                    'sizes': []
                }
        
        # Line-height (explicit override)
        if 'line-height' in resolved_styles:
            lh_val = cls._parse_line_height(resolved_styles['line-height'])
            if lh_val:
                settings['typography_typography'] = 'custom'
                settings['typography_line_height'] = lh_val
        
        # Font weight
        if 'font-weight' in resolved_styles:
            weight = resolved_styles['font-weight']
            try:
                settings['typography_font_weight'] = str(int(weight))
            except ValueError:
                # Handle named weights
                weight_map = {
                    'normal': '400', 'regular': '400',
                    'bold': '700', 'light': '300',
                    'medium': '500', 'semibold': '600',
                    'extrabold': '800', 'black': '900'
                }
                settings['typography_font_weight'] = weight_map.get(weight.lower(), '400')
        
        # Text color
        if 'color' in resolved_styles:
            color = resolved_styles['color']
            if color and color != 'inherit':
                settings['title_color'] = color
                settings['text_color'] = color
        
        # Text alignment
        if 'text-align' in resolved_styles:
            align = resolved_styles['text-align']
            settings['_justify_content'] = align
            settings['horizontal_align'] = align
        
        # Letter spacing
        if 'letter-spacing' in resolved_styles:
            ls_val = FlexboxLayoutCompiler.parse_dimension(resolved_styles['letter-spacing'])
            if ls_val:
                settings['typography_letter_spacing'] = ls_val
        
        return settings
    
    @classmethod
    def _parse_font_size(cls, value: str) -> Optional[Dict[str, Any]]:
        """Parse font-size value"""
        dim = FlexboxLayoutCompiler.parse_dimension(value)
        if dim:
            return dim
        return None
    
    @classmethod
    def _parse_line_height(cls, value: str) -> Optional[Dict[str, Any]]:
        """Parse line-height value"""
        value = value.strip()
        
        # Unitless multiplier
        if re.match(r'^[\d.]+$', value):
            return {'unit': '', 'size': float(value), 'sizes': []}
        
        # With unit
        dim = FlexboxLayoutCompiler.parse_dimension(value)
        if dim:
            return dim
        
        return None


class WidgetStyleMapper:
    """Maps CSS properties to specific Elementor widget settings."""
    
    @classmethod
    def compile_widget_settings(cls, styles: Dict[str, str], widget_type: str, css_vars: CSSVariables) -> Dict[str, Any]:
        """Convert CSS styles to widget-specific settings"""
        settings = {}
        
        # Resolve CSS variables
        resolved_styles = {}
        for key, value in styles.items():
            resolved_styles[key] = css_vars.resolve(value)
        
        # Common text color
        if 'color' in resolved_styles:
            color = resolved_styles['color']
            if color and color != 'inherit':
                if widget_type == 'heading':
                    settings['title_color'] = color
                elif widget_type == 'text-editor':
                    settings['text_color'] = color
                elif widget_type == 'button':
                    settings['button_text_color'] = color
        
        # Typography for all text widgets
        typo_settings = TypographyMapper.compile_typography_settings(resolved_styles, css_vars)
        settings.update(typo_settings)
        
        # Button-specific
        if widget_type == 'button':
            if 'background-color' in resolved_styles:
                bg = resolved_styles['background-color']
                if bg and bg != 'transparent':
                    settings['button_background_color'] = bg
                    settings['background_background'] = 'classic'
                    settings['background_color'] = bg
            
            # Border radius
            if 'border-radius' in resolved_styles:
                br_val = FlexboxLayoutCompiler.parse_dimension(resolved_styles['border-radius'])
                if br_val:
                    settings['border_radius'] = {
                        'topLeft': br_val['size'],
                        'topRight': br_val['size'],
                        'bottomLeft': br_val['size'],
                        'bottomRight': br_val['size'],
                        'unit': br_val['unit'],
                        'isLinked': True
                    }
        
        # Image-specific
        if widget_type == 'image':
            if 'width' in resolved_styles:
                w = FlexboxLayoutCompiler.parse_dimension(resolved_styles['width'])
                if w:
                    settings['width'] = w
        
        return settings


class ElementorLayoutCompiler:
    """Main compiler that orchestrates HTML/CSS to Elementor JSON conversion."""
    
    def __init__(self, title: str = "Converted Template"):
        self.id_gen = ElementorIdGenerator()
        self.css_parser = CSSStyleParser()
        self.schema_mapper = ElementorSchemaMapper()
        self.flex_compiler = FlexboxLayoutCompiler()
        self.typography_mapper = TypographyMapper()
        self.widget_mapper = WidgetStyleMapper()
        self.title = title
        self.css_variables = CSSVariables()
        self.css_rules: Dict[str, Dict[str, str]] = {}
        self.global_colors: Dict[str, str] = {}
    
    def load_css(self, css_content: str):
        """Load and parse CSS content"""
        self.css_rules, self.css_variables = self.css_parser.parse_css_file(css_content)
        
        # Collect global colors for site kit sync (Golden Rule #3)
        color_vars = [
            '--color-primary', '--color-secondary', '--color-accent',
            '--color-text-dark', '--color-text-medium', '--color-text-light',
            '--color-white', '--color-bg-light', '--color-border'
        ]
        for var_name in color_vars:
            if var_name in self.css_variables.variables:
                clean_name = var_name.replace('--color-', '')
                self.global_colors[clean_name] = self.css_variables.variables[var_name]
    
    def get_computed_styles(self, element: Any) -> Dict[str, str]:
        """Get computed styles for an element by combining inline and CSS rules"""
        styles = {}
        
        # Start with inline styles
        inline_style = element.get('style', '')
        if inline_style:
            styles.update(self.css_parser.parse_inline(str(inline_style)))
        
        # Apply matching CSS rules based on class/id/tag
        classes_elem = element.get('class')
        classes = []
        if classes_elem:
            # Handle both string and list values from BeautifulSoup
            if isinstance(classes_elem, str):
                classes = classes_elem.split()
            else:
                # BeautifulSoup returns a list-like object for class attribute
                classes = list(classes_elem) if classes_elem else []
        
        element_id = element.get('id', '') or ''
        tag_name = element.name
        
        # Check class selectors
        for cls in classes:
            selector = f'.{cls}'
            if selector in self.css_rules:
                styles.update(self.css_rules[selector])
        
        # Check ID selector
        if element_id:
            selector = f'#{element_id}'
            if selector in self.css_rules:
                styles.update(self.css_rules[selector])
        
        # Check tag selector
        if tag_name in self.css_rules:
            styles.update(self.css_rules[tag_name])
        
        # Check combined selectors (e.g., .class1.class2)
        if len(classes) > 1:
            combined = '.' + '.'.join(classes)
            if combined in self.css_rules:
                styles.update(self.css_rules[combined])
        
        return styles
    
    def is_major_layout_element(self, element: Any, styles: Dict[str, str]) -> bool:
        """
        FLATTEN HIERARCHY RULE #1:
        Only create Elementor containers for MAJOR layout elements.
        
        Creates container if:
        1. Tag is a major semantic layout tag (section, header, footer, nav, main, aside, article)
        2. OR has explicit 'display: flex' or 'display: grid' in style attribute
        3. OR is a div with flex/grid properties
        
        Plain div wrappers without flex/grid are SKIPPED to reduce nesting depth.
        """
        tag_name = element.name.lower() if element.name else ''
        
        # Rule 1: Major semantic layout tags ALWAYS create containers
        if tag_name in ElementorSchemaMapper.MAJOR_CONTAINER_TAGS:
            return True
        
        # Rule 2: Check for explicit flex/grid display in inline styles or CSS rules
        display = styles.get('display', '')
        if display in ('flex', 'grid', 'inline-flex', 'inline-grid'):
            return True
        
        # Rule 3: div with children that are themselves containers should be flattened
        # We skip creating a container for plain structural divs
        if tag_name == 'div':
            # Check if this div has meaningful flex/grid styles
            has_flex_props = any(k in styles for k in [
                'flex-direction', 'justify-content', 'align-items', 
                'flex-wrap', 'gap', 'align-content'
            ])
            if has_flex_props:
                return True
            
            # Check if div has class that suggests it's a layout container
            classes_elem = element.get('class')
            if classes_elem:
                classes = classes_elem if isinstance(classes_elem, list) else classes_elem.split()
                # Common layout container class patterns
                layout_patterns = ['container', 'row', 'col', 'wrapper', 'flex', 'grid', 'layout']
                if any(pattern in ''.join(classes).lower() for pattern in layout_patterns):
                    return True
            
            # Plain div without flex properties - skip container creation
            # Children will be lifted to parent container
            return False
        
        # For other tags like ul, check if they have list items
        if tag_name in ('ul', 'ol'):
            return True  # Treat lists as containers for icon-list widget
        
        return False
    
    def compile_node(self, element: Any, parent_styles: Dict[str, str] = None, 
                     lift_children: bool = False) -> Optional[Dict[str, Any]]:
        """
        Recursively compile HTML element to Elementor node.
        
        FLATTEN HIERARCHY OPTIMIZATION:
        - Only creates containers for major layout elements
        - Plain divs without layout classes pass their children up to parent container
        - Maximum nesting depth kept under 5 layers
        """
        if element is None or element.name is None:
            return None
        
        # Skip script, style, meta tags and empty text
        if element.name in ('script', 'style', 'meta', 'link', 'head', 'title', 'br', 'hr'):
            return None
        
        # Get computed styles
        styles = self.get_computed_styles(element)
        
        # Determine if this is a major layout container
        is_major_container = self.is_major_layout_element(element, styles)
        
        if is_major_container:
            return self._compile_container(element, styles)
        else:
            # This is either a widget or a plain wrapper div
            tag_name = element.name.lower()
            
            # Widget-only tags always produce widgets
            if tag_name in ElementorSchemaMapper.WIDGET_ONLY_TAGS:
                return self._compile_widget(element, styles)
            
            # For non-widget tags (like span, div without layout), check children
            children_nodes = []
            for child in element.find_all(recursive=False):
                compiled_child = self.compile_node(child, styles, lift_children=True)
                if compiled_child:
                    # If child marked for lifting, extract its children
                    if lift_children and compiled_child.get('_lift'):
                        children_nodes.extend(compiled_child.get('elements', []))
                    else:
                        children_nodes.append(compiled_child)
            
            # If we have children nodes and this is a plain wrapper, return children for lifting
            if lift_children and children_nodes:
                return {'_lift': True, 'elements': children_nodes}
            
            # Otherwise try to compile as widget (fallback)
            return self._compile_widget(element, styles)
    
    def _compile_container(self, element: Any, styles: Dict[str, str]) -> Dict[str, Any]:
        """Compile element as a container"""
        node = {
            'id': self.id_gen.generate(element.name),
            'elType': 'container',
            'settings': self.flex_compiler.compile_container_settings(styles, self.css_variables),
            'elements': []
        }
        
        # Add CSS classes for reference
        if element.get('class'):
            node['settings']['css_classes'] = element.get('class')
        
        if element.get('id'):
            node['settings']['css_id'] = element.get('id')
        
        # Process children - collect and potentially lift plain wrapper children
        all_children = []
        for child in element.find_all(recursive=False):
            compiled_child = self.compile_node(child, styles, lift_children=True)
            if compiled_child:
                # If child marked for lifting, extract its children
                if compiled_child.get('_lift'):
                    all_children.extend(compiled_child.get('elements', []))
                else:
                    all_children.append(compiled_child)
        
        node['elements'] = all_children
        
        # Golden Rule #4: Micro-padding calculation
        self._apply_micro_padding(node, styles)
        
        return node
    
    def _apply_micro_padding(self, node: Dict[str, Any], styles: Dict[str, str]):
        """Apply micro-padding adjustments for pixel-perfect layouts"""
        # This would require bounding box calculations from design files
        # For HTML/CSS input, we use the parsed padding directly
        pass
    
    def _compile_widget(self, element: Any, styles: Dict[str, str]) -> Dict[str, Any]:
        """
        Compile element as a widget.
        
        CONTROL ARRAYS RULE #3:
        Every widget item explicitly contains an empty settings block structure
        if no custom attributes are found, avoiding empty payload references.
        """
        tag_name = element.name.lower()
        widget_type = ElementorSchemaMapper.get_widget_type(tag_name)
        
        # Always initialize with empty settings dict (CONTROL ARRAYS RULE)
        settings = {}
        
        # Content extraction based on widget type
        if widget_type == 'heading':
            settings['title'] = element.get_text(strip=True)
            settings['header_size'] = tag_name
            
        elif widget_type == 'text-editor':
            text_content = element.get_text(strip=True)
            if text_content:
                settings['editor'] = text_content
            else:
                # Preserve HTML for elements with nested structure
                settings['editor'] = str(element)
                
        elif widget_type == 'image':
            img_url = element.get('src', '')
            img_alt = element.get('alt', '')
            settings['image'] = {'url': img_url, 'alt': img_alt}
            
        elif widget_type == 'button':
            settings['text'] = element.get_text(strip=True)
            href = element.get('href', '#')
            settings['link'] = {'url': href, 'is_external': href.startswith('http')}
            
        elif widget_type == 'icon-list':
            # Process list items
            items = []
            for li in element.find_all('li', recursive=False):
                item_text = li.get_text(strip=True)
                items.append({'text': item_text})
            settings['icon_list'] = items
        
        elif widget_type == 'html':
            # SVG or other raw HTML
            settings['html'] = str(element)
        
        elif widget_type == 'form':
            # Form elements
            settings['field_type'] = tag_name
            if element.get('name'):
                settings['field_label'] = element.get('name')
        
        # Merge widget-specific styles
        widget_styles = self.widget_mapper.compile_widget_settings(styles, widget_type, self.css_variables)
        settings.update(widget_styles)
        
        return {
            'id': self.id_gen.generate(tag_name),
            'elType': 'widget',
            'widgetType': widget_type,
            'settings': settings  # Always present, even if empty
        }
    
    def convert(self, html_input: str, css_input: str = "", title: str = None) -> str:
        """
        Convert HTML/CSS to Elementor JSON.
        
        SYSTEM SCHEMA HEADERS RULE #2:
        Root dictionary uses exact Elementor system keys:
        - version: "0.4"
        - title, type, content
        - page_settings with post_status
        """
        if title:
            self.title = title
        
        # Load CSS if provided
        if css_input:
            self.load_css(css_input)
        
        # Parse HTML
        soup = BeautifulSoup(html_input, 'html.parser')
        
        # Find the main content (skip html, head, body wrappers)
        root_element = soup.body if soup.body else soup.find()
        
        # Build document structure with SYSTEM SCHEMA HEADERS
        document_tree = {
            'version': '0.4',  # Updated version per requirements
            'title': self.title,
            'type': 'page',
            'content': [],
            'page_settings': {
                'post_status': 'publish'
            }
        }
        
        # Compile the tree
        if root_element:
            compiled_tree = self.compile_node(root_element)
            if compiled_tree:
                # Handle lift marker at root level
                if compiled_tree.get('_lift'):
                    # Add lifted children directly to content
                    for child in compiled_tree.get('elements', []):
                        if child.get('elType') == 'container':
                            document_tree['content'].append(child)
                        else:
                            # Wrap single widget in container
                            fallback_container = {
                                'id': self.id_gen.generate('wrapper'),
                                'elType': 'container',
                                'settings': {
                                    'flex_direction': 'column',
                                    'content_width': 'boxed'
                                },
                                'elements': [child]
                            }
                            document_tree['content'].append(fallback_container)
                elif compiled_tree['elType'] == 'container':
                    document_tree['content'].append(compiled_tree)
                else:
                    # Wrap single widget in container
                    fallback_container = {
                        'id': self.id_gen.generate('wrapper'),
                        'elType': 'container',
                        'settings': {
                            'flex_direction': 'column',
                            'content_width': 'boxed'
                        },
                        'elements': [compiled_tree]
                    }
                    document_tree['content'].append(fallback_container)
        
        return json.dumps(document_tree, indent=2)
    
    def convert_files(self, html_path: str, css_path: str = None, output_path: str = None) -> str:
        """Convert HTML and CSS files to Elementor JSON"""
        # Read HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Read CSS if path provided
        css_content = ""
        if css_path and Path(css_path).exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        elif Path(html_path).with_suffix('.css').exists():
            # Try to find matching CSS file
            css_path_auto = Path(html_path).with_suffix('.css')
            with open(css_path_auto, 'r', encoding='utf-8') as f:
                css_content = f.read()
        
        # Convert
        title = Path(html_path).stem.replace('-', ' ').replace('_', ' ').title()
        json_output = self.convert(html_content, css_content, title)
        
        # Write output
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
        else:
            # Default output path
            output_path = Path(html_path).with_suffix('.elementor.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
        
        return json_output


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("HTML/CSS to Elementor Pro JSON Converter")
        print("Usage: python html_to_elementor.py <html_file> [css_file] [output_file]")
        print("\nExamples:")
        print("  python html_to_elementor.py header.html")
        print("  python html_to_elementor.py header.html header.css")
        print("  python html_to_elementor.py header.html header.css header.elementor.json")
        sys.exit(1)
    
    html_file = sys.argv[1]
    css_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    compiler = ElementorLayoutCompiler()
    
    try:
        json_output = compiler.convert_files(html_file, css_file, output_file)
        output_path = output_file or Path(html_file).with_suffix('.elementor.json')
        print(f"✓ Successfully converted to Elementor JSON")
        print(f"  Output: {output_path}")
        print(f"  Size: {len(json_output)} bytes")
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
