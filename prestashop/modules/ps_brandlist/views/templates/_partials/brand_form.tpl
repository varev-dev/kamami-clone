{**
 * Kamami theme - Brand list carousel for footer
 * Displays manufacturer logos in a horizontal scrolling carousel
 *}

{if $brands}
  <div class="dfx_manufacturer manufacturer-carousel">
    <div class="manufacturer-carousel-inner">
      {foreach from=$brands item=brand}
        <div class="image_manufacture">
          <a href="{$brand.link}" title="{$brand.name}" aria-label="{$brand.name}">
            {* Check if brand has a custom image (image is numeric ID) or use default/fallback *}
            {if $brand.image|is_numeric}
              {* Custom manufacturer image exists *}
              <img class="img-fluid" loading="lazy" src="{$urls.base_url}img/m/{$brand.image}-medium_default.jpg"
                alt="{$brand.name}" width="129" height="89"
                onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
              <span class="brand-name" style="display:none;">{$brand.name}</span>
            {else}
              {* No custom image, show brand name as text *}
              <span class="brand-name">{$brand.name}</span>
            {/if}
          </a>
        </div>
      {/foreach}
    </div>

    <div class="manufacturer-nav">
      <button type="button" class="manufacturer-prev" aria-label="{l s='Previous' d='Shop.Theme.Actions'}">
        <i class="material-icons">chevron_left</i>
      </button>
      <button type="button" class="manufacturer-next" aria-label="{l s='Next' d='Shop.Theme.Actions'}">
        <i class="material-icons">chevron_right</i>
      </button>
    </div>
  </div>
{/if}