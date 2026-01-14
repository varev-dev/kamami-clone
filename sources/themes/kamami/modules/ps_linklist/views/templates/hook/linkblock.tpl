{**
 * Kamami theme - Link list block for footer
 * Based on kamami.pl footer layout with collapsible mobile sections
 *}

{foreach $linkBlocks as $linkBlock}
<div class="col-md-3 links">
  {* Desktop title *}
  <h4 class="hidden-sm-down">{$linkBlock.title|escape:'html':'UTF-8'}</h4>

  {* Mobile collapsible title *}
  <div class="title clearfix hidden-md-up" data-target="#footer_sub_menu_{$linkBlock.id}" data-toggle="collapse">
    <h4>{$linkBlock.title|escape:'html':'UTF-8'}</h4>
    <span class="float-xs-right">
      <span class="navbar-toggler collapse-icons">
        <i class="material-icons add">add</i>
        <i class="material-icons remove">remove</i>
      </span>
    </span>
  </div>

  <ul id="footer_sub_menu_{$linkBlock.id}" class="collapse">
    {foreach $linkBlock.links as $link}
    <li>
      <a
        id="{$link.id}-{$linkBlock.id}"
        class="{$link.class}"
        href="{$link.url|escape:'html':'UTF-8'}"
        title="{$link.description|escape:'html':'UTF-8'}"
        {if !empty($link.target)} target="{$link.target|escape:'html':'UTF-8'}" {/if}
      >
        {$link.title|escape:'html':'UTF-8'}
      </a>
    </li>
    {/foreach}
  </ul>
</div>
{/foreach}

