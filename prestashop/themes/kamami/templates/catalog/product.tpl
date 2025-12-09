{**
 * Kamami theme product page template
 * Overrides classic theme product.tpl for custom page-footer
 *}
{extends file='parent:catalog/product.tpl'}

{block name='page_footer_container'}
  <footer class="page-footer">
    {block name='page_footer'}
      {include file='_partials/page-footer-content.tpl'}
    {/block}
  </footer>
{/block}

