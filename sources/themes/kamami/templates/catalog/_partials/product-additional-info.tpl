<div class="product-additional-info js-product-additional-info">
  {hook h='displayProductAdditionalInfo' product=$product}

  {if isset($groups) && $groups}
    {foreach from=$groups key=id_attribute_group item=group}
      {if !empty($group.attributes)}
        <div class="jzrelprods-wrapper">
          <span class="jzrelprods-caption">{$group.name}:</span>
          <div class="jzrelprods-buttons">
            {foreach from=$group.attributes key=id_attribute item=group_attribute}
              {if $group_attribute.selected}
                <div class="jzrelprods-button-disabled" title="{$group_attribute.name}">
                  {$group_attribute.name}
                </div>
              {else}
                <button type="button" class="jzrelprods-button js-variant-selector" data-product-attribute="{$id_attribute_group}"
                  data-attribute-value="{$id_attribute}" title="{$group_attribute.name}"
                  {if isset($group_attribute.html_color_code) && $group_attribute.html_color_code}
                  style="background-color: {$group_attribute.html_color_code};" {/if}>
                  {$group_attribute.name}
                </button>
              {/if}
            {/foreach}
          </div>
        </div>
      {/if}
    {/foreach}
  {/if}
</div>