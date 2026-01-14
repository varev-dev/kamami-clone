{**
 * Kamami theme - Store contact information block for footer
 * Based on kamami.pl footer layout
 *}

<div class="block-contact col-md-3 links">
  {* Mobile collapsible title *}
  <div class="title clearfix hidden-md-up" data-target="#contact-infos" data-toggle="collapse">
    <h4>{l s='Store information' d='Shop.Theme.Global'}</h4>
    <span class="float-xs-right">
      <span class="navbar-toggler collapse-icons">
        <i class="material-icons add">add</i>
        <i class="material-icons remove">remove</i>
      </span>
    </span>
  </div>

  {* Desktop title *}
  <h4 class="hidden-sm-down">{l s='Store information' d='Shop.Theme.Global'}</h4>

  <ul id="contact-infos" class="collapse">
    {* Address *}
    <li class="addressicon">
      {$contact_infos.address.formatted nofilter}
    </li>

    {* Phone *}
    {if $contact_infos.phone}
      <li class="contacticon">
        {l s='Call us:' d='Shop.Theme.Global'}
        <a href="tel:{$contact_infos.phone|replace:' ':''}">{$contact_infos.phone}</a>
      </li>
    {/if}

    {* Fax *}
    {if $contact_infos.fax}
      <li class="faxicon">
        {l s='Fax:' d='Shop.Theme.Global'}
        <span>{$contact_infos.fax}</span>
      </li>
    {/if}

    {* Email *}
    {if $contact_infos.email && $display_email}
      <li class="emailicon">
        {l s='Email us:' d='Shop.Theme.Global'}
        <a href="mailto:{$contact_infos.email}">{$contact_infos.email}</a>
      </li>
    {/if}
  </ul>
</div>
