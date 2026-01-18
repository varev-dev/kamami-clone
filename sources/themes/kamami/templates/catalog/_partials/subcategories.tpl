{**
 * Subcategories template
 *}
{if !empty($subcategories)}
  {if (isset($display_subcategories) && $display_subcategories eq 1) || !isset($display_subcategories)}
    <div id="subcategories" class="card card-block">
      <h2 class="subcategory-heading">{l s='Podkategorie' d='Shop.Theme.Category'}</h2>

      <ul class="subcategories-list">
        {foreach from=$subcategories item=subcategory}
          <li>
            <div class="subcategory-image">
              <a href="{$link->getCategoryLink($subcategory.id_category, $subcategory.link_rewrite)|escape:'html':'UTF-8'}" title="{$subcategory.name|escape:'html':'UTF-8'}" class="img">
                {if !empty($subcategory.image.small.url)}
                  <img class="replace-2x" src="{$subcategory.image.small.url}" alt="{$subcategory.name|escape:'html':'UTF-8'}" loading="lazy" width="125" height="125"/>
                {elseif !empty($subcategory.image.medium.url)}
                  <img class="replace-2x" src="{$subcategory.image.medium.url}" alt="{$subcategory.name|escape:'html':'UTF-8'}" loading="lazy" width="125" height="125"/>
                {/if}
              </a>
            </div>

            <h3><a class="subcategory-name" href="{$link->getCategoryLink($subcategory.id_category, $subcategory.link_rewrite)|escape:'html':'UTF-8'}">{$subcategory.name|escape:'html':'UTF-8'}</a></h3>
          </li>
        {/foreach}
      </ul>
    </div>
  {/if}
{/if}

