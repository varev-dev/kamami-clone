{**
 * Sort orders template
 *}
<button class="btn-unstyle select-title" rel="nofollow" data-toggle="dropdown" aria-label="{l s='Sort by selection' d='Shop.Theme.Global'}" aria-haspopup="true" aria-expanded="false">
  {if $listing.sort_selected}{$listing.sort_selected}{else}{l s='Select' d='Shop.Theme.Actions'}{/if}
  <i class="material-icons arrow_drop_down float-xs-right">&#xE5C5;</i>
</button>

<div class="dropdown-menu">
  {foreach from=$listing.sort_orders item=sort_order}
    <a
      rel="nofollow"
      href="{$sort_order.url}"
      class="select-list {['current' => $sort_order.current, 'js-search-link' => true]|classnames}"
    >
      {$sort_order.label}
    </a>
  {/foreach}
</div>

