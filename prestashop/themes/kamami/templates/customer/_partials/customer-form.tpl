{block name='customer_form'}
  {block name='customer_form_errors'}
    {include file='_partials/form-errors.tpl' errors=$errors['']}
  {/block}

  <form action="{block name='customer_form_actionurl'}{$action}{/block}" id="customer-form" class="js-customer-form"
    method="post">
    <section>
      {block "form_fields"}
        {foreach from=$formFields item="field"}
          {block "form_field"}
            {if $field.type == 'text' && ($field.name == 'firstname' || $field.name == 'lastname')}
              <div class="form-group-w form-group-w-{$field.name}">
                <div class="form-group row form-group-fr">
                  <label class="form-control-label{if $field.required} required{/if}" for="field-{$field.name}">
                    {$field.label}
                  </label>
                  <div class="">
                    <input id="field-{$field.name}" class="form-control" name="{$field.name}" type="text" value="{$field.value}"
                      {if $field.required}required{/if}>
                    {if isset($field.availableValues.comment)}
                      <span class="form-control-comment form-control-comment-{$field.name}">
                        {$field.availableValues.comment}
                      </span>
                    {/if}
                  </div>
                </div>
                <div class="form-control-comment">
                </div>
              </div>
            {elseif $field.type == 'email'}
              <div class="form-group-w form-group-w-email">
                <div class="form-group row form-group-fr">
                  <label class="form-control-label{if $field.required} required{/if}" for="field-{$field.name}">
                    {$field.label}
                  </label>
                  <div class="">
                    <input id="field-{$field.name}" class="form-control" name="{$field.name}" type="email" value="{$field.value}"
                      {if $field.required}required{/if}>
                  </div>
                </div>
                <div class="form-control-comment">
                </div>
              </div>
            {elseif $field.type == 'password'}
              {if $field.name == 'new_password'}
                <div class="form-group-w form-group-w-new_password">
                  <div class="form-group row form-group-fr">
                    <label class="form-control-label{if $field.required} required{/if}" for="field-{$field.name}">
                      {$field.label}
                    </label>
                    <div class="">
                      <div class="input-group js-parent-focus">
                        <input id="field-{$field.name}" class="form-control js-child-focus js-visible-password" name="{$field.name}"
                          title="{l s='Co najmniej 5 znaków' d='Shop.Forms.Help'}"
                          aria-label="{l s='Hasło musi zawierać przynajmniej 5 znaków' d='Shop.Forms.Help'}" type="password"
                          {if $field.autocomplete}autocomplete="{$field.autocomplete}" {/if} value=""
                          pattern=".{literal}{{/literal}5,{literal}}{/literal}" {if $field.required}required{/if}>
                        <span class="input-group-btn show-password">
                          <button class="btn" type="button" data-action="show-password"
                            data-text-show="{l s='Pokaż' d='Shop.Theme.Actions'}"
                            data-text-hide="{l s='Ukryj' d='Shop.Theme.Actions'}">
                            {l s='Pokaż' d='Shop.Theme.Actions'}
                          </button>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="form-control-comment">
                    {if !$field.required}
                      {l s='Opcjonalne' d='Shop.Forms.Labels'}
                    {/if}
                  </div>
                </div>
              {else}
                <div class="form-group-w form-group-w-password">
                  <div class="form-group row form-group-fr">
                    <label class="form-control-label{if $field.required} required{/if}" for="field-{$field.name}">
                      {$field.label}
                    </label>
                    <div class="">
                      <div class="input-group js-parent-focus">
                        <input id="field-{$field.name}" class="form-control js-child-focus js-visible-password" name="{$field.name}"
                          title="{l s='Co najmniej 5 znaków' d='Shop.Forms.Help'}"
                          aria-label="{l s='Hasło musi zawierać przynajmniej 5 znaków' d='Shop.Forms.Help'}" type="password"
                          {if $field.autocomplete}autocomplete="{$field.autocomplete}" {/if} value=""
                          pattern=".{literal}{{/literal}5,{literal}}{/literal}" {if $field.required}required{/if}>
                        <span class="input-group-btn show-password">
                          <button class="btn" type="button" data-action="show-password"
                            data-text-show="{l s='Pokaż' d='Shop.Theme.Actions'}"
                            data-text-hide="{l s='Ukryj' d='Shop.Theme.Actions'}">
                            {l s='Pokaż' d='Shop.Theme.Actions'}
                          </button>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="form-control-comment">
                  </div>
                </div>
              {/if}
            {elseif $field.type == 'checkbox'}
              {if $field.name == 'optin'}
                {* Skip optin field (partner offers) - hidden *}
              {else}
                <div class="form-group-w form-group-w-{$field.name}">
                  <div class="form-group row">
                    <label class="form-control-label{if $field.required} required{/if}" for="field-{$field.name}">
                    </label>
                    <div class="">
                      <span class="custom-checkbox">
                        <input name="{$field.name}" type="checkbox" value="1" {if $field.value}checked="checked" {/if}
                          {if $field.required}required{/if}>
                        <span><i class="material-icons rtl-no-flip checkbox-checked">&#xE5CA;</i></span>
                        <label>
                          {if $field.name == 'customer_privacy'}
                            {l s='Oświadczam, że zapoznałem/am się i akceptuję politykę przetwarzania danych osobowych' d='Shop.Forms.Labels'}<br>
                            <em>
                              <p>
                                <em>{l s='Udostępnione przez Ciebie dane osobowe są wykorzystywane w celu udzielania odpowiedzi na zapytania, przetwarzania zamówień lub umożliwiania dostępu do konkretnych informacji. Przysługuje Ci prawo do modyfikowania oraz usuwania wszelkich danych osobowych zamieszczonych na stronie „Moje konto".' d='Shop.Forms.Labels'}</em>
                              </p>
                              <p><a href="{$link->getCMSLink(2)}"><span
                                    style="color:#d0121a;">{l s='Regulamin przetwarzania danych osobowych' d='Shop.Forms.Labels'}</span></a>
                              </p>
                            </em>
                          {elseif $field.name == 'newsletter'}
                            {l s='Zapisz się do newslettera' d='Shop.Forms.Labels'}<br>
                            <em>{l s='Chcesz być na bieżąco z nowościami elektronicznymi oraz specjalnymi ofertami z naszego sklepu? Zapisz się do newslettera!' d='Shop.Forms.Labels'}</em>
                          {elseif $field.name == 'psgdpr' || $field.name == 'psgdpr_psgdpr'}
                            {l s='Akceptuję ogólne warunki użytkowania i politykę prywatności' d='Shop.Forms.Labels'}
                          {else}
                            {$field.label nofilter}
                          {/if}
                        </label>
                      </span>
                    </div>
                  </div>
                  <div class="form-control-comment">
                  </div>
                </div>
              {/if}
            {elseif $field.type == 'birthday' || $field.name == 'birthday'}
              {* Skip birthday field - hidden *}
            {else}
              {form_field field=$field}
            {/if}
          {/block}
        {/foreach}
      {/block}
    </section>

    {block name='customer_form_footer'}
      <footer class="form-footer clearfix">
        <input type="hidden" name="submitCreate" value="1">
        {block "form_buttons"}
          <button class="btn btn-primary form-control-submit float-xs-right" data-link-action="save-customer" type="submit">
            {l s='Zapisz' d='Shop.Theme.Actions'}
          </button>
        {/block}
      </footer>
    {/block}

  </form>
{/block}