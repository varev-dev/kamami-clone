{**
 * Category header template
 *}
<h1 id="js-product-list-header" class="h2">Kategoria: {$category.name|upper}</h1>
{if $listing.pagination.items_shown_from == 1}
  <div>
    <h1>{$category.name}</h1>
    {if $category.description}
      <p>{$category.description nofilter}</p>
    {/if}
  </div>
{/if}

