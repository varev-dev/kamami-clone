{**
 * Products top controls template
 *}
<div id="js-product-list-top" class="products-selection row d-flex justify-content-center flex-wrap">
  <div class="col-xs-12 col-sm-12 col-md-12 col-lg-4 faceted_padding_top faceted_btn">
    <p class="products-counter">
      {l s='Liczba produktów: %count%' d='Shop.Theme.Catalog' sprintf=['%count%' => $listing.pagination.total_items]}
    </p>
  </div>

  <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2 faceted_padding_top hidden-xs-down prod-list-view-sel">
    <ul class="redfoxGridList">
      <li id="grid" class="pull-left selected_grid">
        <a rel="nofollow" href="javascript:void(0)" title="{l s='Widok kafelków' d='Shop.Theme.Catalog'}">
          <i class="redfox-view-thumb"></i>
        </a>
      </li>
      <li id="list" class="pull-left">
        <a rel="nofollow" href="javascript:void(0)" title="{l s='Widok listy' d='Shop.Theme.Catalog'}">
          <i class="redfox-view-list-large"></i>
        </a>
      </li>
    </ul>
  </div>

  <div class="col-xs-4 col-sm-4 col-md-4 col-lg-2 faceted_padding_top">
    <div class="row">
      <span class="col-sm-7 col-md-7 col-lg-7 hidden-xs-down sort-by">{l s='Ilość:' d='Shop.Theme.Catalog'}</span>
      {* Calculate items per page from pagination data *}
      {if $listing.pagination.current_page == $listing.pagination.pages_count}
        {* On last page, calculate from actual items shown *}
        {assign var="current_items_per_page" value=($listing.pagination.items_shown_to - $listing.pagination.items_shown_from + 1)}
      {else}
        {* On other pages, calculate from range *}
        {assign var="current_items_per_page" value=($listing.pagination.items_shown_to - $listing.pagination.items_shown_from + 1)}
      {/if}
      {* Fallback to default if calculation fails *}
      {if $current_items_per_page <= 0 || $current_items_per_page > 100}
        {assign var="current_items_per_page" value=20}
      {/if}
      <select name="n" id="pppsel" style="display: none;">
        <option value="20" {if $current_items_per_page == 20}selected="true" {/if}>20</option>
        <option value="50" {if $current_items_per_page == 50}selected="true" {/if}>50</option>
        <option value="100" {if $current_items_per_page == 100}selected="true" {/if}>100</option>
      </select>

      <div class="col-sm-5 col-xs-12 col-md-5 col-lg-5 products-sort-order dropdown">
        <button id="pppbtn" class="btn-unstyle select-title" rel="nofollow" data-toggle="dropdown"
          aria-label="{l s='Sort by selection' d='Shop.Theme.Global'}" aria-haspopup="true" aria-expanded="true">
          <span id="pppbtn-text">{$current_items_per_page}</span>
          <i class="material-icons arrow_drop_down float-xs-right">&#xE5C5;</i>
        </button>

        <div class="dropdown-menu">
          <a href="#" class="select-list ppiselval" onclick="ppisel(event, 20);">20</a>
          <a href="#" class="select-list ppiselval" onclick="ppisel(event, 50);">50</a>
          <a href="#" class="select-list ppiselval" onclick="ppisel(event, 100);">100</a>
        </div>
      </div>
    </div>
  </div>

  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-4 faceted_padding_top">
    <div class="row sort-by-row">
      <span class="col-sm-4 col-md-4 col-lg-4 hidden-xs-down sort-by">{l s='Sortuj wg:' d='Shop.Theme.Global'}</span>
      <div class="col-sm-8 col-xs-12 col-md-8 col-lg-8 products-sort-order dropdown">
        {block name='sort_by'}
          {include file='catalog/_partials/sort-orders.tpl' sort_orders=$listing.sort_orders}
        {/block}
      </div>
    </div>
  </div>
</div>