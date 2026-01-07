{**
 * Category listing template
 *}
{extends file='catalog/listing/product-list.tpl'}

{block name='product_list_header'}
    {include file='catalog/_partials/category-header.tpl' listing=$listing category=$category}
{/block}

