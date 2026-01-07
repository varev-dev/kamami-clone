{**
 * Pagination template
 *}
<nav class="pagination">
  <div class="col-lg-4 col-md-12 col-sm-12 pagi-numbers">
    {block name='pagination_summary'}
      {l s='Pokazano %from%-%to% z %total% pozycji' d='Shop.Theme.Catalog' sprintf=['%from%' => $pagination.items_shown_from, '%to%' => $pagination.items_shown_to, '%total%' => $pagination.total_items]}
    {/block}
  </div>

  <div class="col-lg-8 col-md-12 col-sm-12">
    {block name='pagination_page_list'}
      {if $pagination.should_be_displayed}
        <ul class="page-list clearfix text-sm-center">
          {foreach from=$pagination.pages item="page"}
            <li {if $page.current} class="current" {/if}>
              {if $page.type === 'spacer'}
                <span class="spacer">…</span>
              {else}
                <a
                  rel="{if $page.type === 'previous'}prev{elseif $page.type === 'next'}next{else}nofollow{/if}"
                  href="{$page.url}"
                  class="{if $page.type === 'previous'}previous {elseif $page.type === 'next'}next {/if}{['disabled' => !$page.clickable, 'js-search-link' => true]|classnames}"
                >
                  {if $page.type === 'previous'}
                    <span class="pag-text">{l s='Poprzednia' d='Shop.Theme.Actions'}</span><i class="material-icons">&#xE314;</i>
                  {elseif $page.type === 'next'}
                    <span class="pag-text">{l s='Następna' d='Shop.Theme.Actions'}</span><i class="material-icons">&#xE315;</i>
                  {else}
                    {$page.page}
                  {/if}
                </a>
              {/if}
            </li>
          {/foreach}
        </ul>
      {/if}
    {/block}
  </div>
</nav>

