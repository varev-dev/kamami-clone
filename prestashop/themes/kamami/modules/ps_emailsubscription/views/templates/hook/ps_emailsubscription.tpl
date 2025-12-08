{**
 * Kamami theme - Newsletter subscription block for footer
 * Based on kamami.pl footer layout with collapsible mobile section
 *}

<div class="block_newsletter col-md-3 links" id="blockEmailSubscription_{$hookName}">
  <div class="footer_news">
    {* Desktop title *}
    <h4 class="hidden-sm-down">{l s='Newsletter' d='Shop.Theme.Global'}</h4>

    {* Mobile collapsible title *}
    <div class="title clearfix hidden-md-up" data-target="#footer_sub_menu_newsletter" data-toggle="collapse">
      <h4>{l s='Newsletter' d='Shop.Theme.Global'}</h4>
      <span class="float-xs-right">
        <span class="navbar-toggler collapse-icons">
          <i class="material-icons add">add</i>
          <i class="material-icons remove">remove</i>
        </span>
      </span>
    </div>

    <ul id="footer_sub_menu_newsletter" class="collapse">
      <li>
        <p class="col-md-12 col-xs-12 newsletter-content">
          Chcesz być na bieżąco z nowościami elektronicznymi oraz specjalnymi ofertami z naszego sklepu? Zapisz się do
          newslettera!
        </p>
      </li>

      <li>
        <form action="{$urls.current_url}#footer" method="post">
          <div class="row">
            <div class="col-xs-12">
              <div class="input-wrapper">
                <input name="email" type="email" value="{$value}"
                  placeholder="{l s='Your email address' d='Shop.Forms.Labels'}"
                  aria-labelledby="block-newsletter-label" required>
                <button class="btn btn-primary float-xs-left" name="submitNewsletter" type="submit" value=""
                  aria-label="{l s='Subscribe' d='Shop.Theme.Actions'}">
                  <i class="material-icons">mail_outline</i>
                </button>
              </div>
              <input type="hidden" name="blockHookName" value="{$hookName}">
              <input type="hidden" name="action" value="0">
              <div class="clearfix"></div>
            </div>

            <div class="col-xs-12">
              {if $msg}
                <p class="alert {if $nw_error}alert-danger{else}alert-success{/if}">
                  {$msg}
                </p>
              {/if}

              {hook h='displayNewsletterRegistration'}

              {* GDPR Consent Checkbox *}
              {if isset($id_module)}
                {hook h='displayGDPRConsent' id_module=$id_module}
              {/if}
            </div>
          </div>
        </form>
      </li>
    </ul>
  </div>
</div>