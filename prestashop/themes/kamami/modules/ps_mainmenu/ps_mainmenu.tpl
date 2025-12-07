<div class="main-menu hidden-md-down">
  <div class="container">
    <ul class="jetmenu">
      {foreach from=$menu.children item=node name=menuloop}
        <li class="redfoxmenu_li menulink-{$smarty.foreach.menuloop.index}" data-menu="{$smarty.foreach.menuloop.index}">
          <a href="{$node.url}" title="{$node.label}" {if $node.open_in_new_window}target="_blank" {/if}>
            {$node.label}
          </a>
        </li>
      {/foreach}
    </ul>
  </div>
</div>