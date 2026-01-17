<div class="contact-rich">
  <h4>{l s='Store information' d='Shop.Theme.Global'}</h4>
  
  {* Address Block *}
  <div class="block">
    <div class="icon"><i class="redfox-location"></i></div>
    <div class="data">
      {$contact_infos.address.formatted nofilter}
      {if $contact_infos.details}
        <br>{$contact_infos.details|nl2br nofilter}
      {/if}
    </div>
  </div>
  
  {* Phone Block *}
  {if $contact_infos.phone}
    <hr>
    <div class="block">
      <div class="icon"><i class="redfox-phone"></i></div>
      <div class="data">
        {l s='Call us:' d='Shop.Theme.Global'}<br>
        <a href="tel:{$contact_infos.phone|replace:' ':''}">{$contact_infos.phone}</a>
      </div>
    </div>
  {/if}
  
  {* Email Block *}
  {if $contact_infos.email && $display_email}
    <hr>
    <div class="block">
      <div class="icon"><i class="redfox-mail"></i></div>
      <div class="data email">
        {l s='Email us:' d='Shop.Theme.Global'}<br>
      </div>
      <a href="mailto:{$contact_infos.email}">{$contact_infos.email}</a>
    </div>
  {/if}
</div>
