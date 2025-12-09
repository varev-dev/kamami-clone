{if $homeslider.slides}
  <div class="simple-slider">
    <div id="dfx-slider" class="dfximagecarousel owl-carousel owl-theme">
      {foreach from=$homeslider.slides item=slide}
        <div class="item posleft">
          {if !empty($slide.url)}
            <a href="{$slide.url}" aria-label="{$slide.legend|escape}">
            {/if}
            <img class="owl-lazy"
              src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20900%20532%22%3E%3C/svg%3E"
              data-src="{$slide.image_url}" alt="{$slide.legend|escape}" title="{$slide.legend|escape}"
              style="width: 100%; height: 100%; object-fit: cover;" {if isset($slide.size)} {$slide.size}{/if}>
            {if !empty($slide.url)}
            </a>
          {/if}
        </div>
      {/foreach}
    </div>
    <div class="slide-progress"></div>
  </div>
{/if}