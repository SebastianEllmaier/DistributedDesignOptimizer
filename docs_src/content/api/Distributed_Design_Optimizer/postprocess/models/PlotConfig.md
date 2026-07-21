---
title: PlotConfig
---

← Back to [models](index.md)

# PlotConfig

**Source:** [Distributed_Design_Optimizer\postprocess\models\PlotConfig.py](PlotConfig_source.md)

Dataclass models for plot configuration, fonts, lines, and reference lines.

## Classes

### FontConfig

> Font configuration for a single text element.

#### Attributes

> `family`: str  
> `size`: int  
> `weight`: str  

### LineConfig

> Configuration for a single plot line.

#### Attributes

> `item_path`: str  
> `label`: str  
> `style`: str  
> `width`: float  
> `color`: str | None  
> `markers`: bool  

### ReferenceLine

> A horizontal reference line on the plot.

#### Attributes

> `name`: str  
> `value`: float  
> `color`: str  
> `style`: str  
> `width`: float  
> `enabled`: bool  
> `markers`: bool  

### PlotConfig

> Complete plot configuration state.

#### Attributes

> `plot_type`: str  
> `log_scale`: bool  
> `x_axis_type`: str  
> `show_legend`: bool  
> `show_grid`: bool  
> `legend_position`: str  
> `custom_x_label`: str  
> `custom_y_label`: str  
> `custom_title`: str  
> `stacked_titles`: list[str]  
> `stacked_y_labels`: list[str]  
> `independent_y_labels`: list[str]  
> `title_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `x_label_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `y_label_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `legend_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `x_tick_label_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `y_tick_label_font`: [FontConfig](PlotConfig.md#fontconfig)  
> `x_tick_size`: int  
> `y_tick_size`: int  
> `line_configs`: dict[str, [LineConfig](PlotConfig.md#lineconfig)]  
> `reference_lines`: list[[ReferenceLine](PlotConfig.md#referenceline)]  

