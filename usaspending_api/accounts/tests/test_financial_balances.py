import pytest

from model_mommy import mommy
from rest_framework import status


@pytest.fixture
def financial_balances_models():
    sub = mommy.make('submissions.SubmissionAttributes', reporting_fiscal_year=2016)
    agency1_toptier = mommy.make('references.TopTierAgency', toptier_agency_id=123)
    agency1 = mommy.make('references.Agency', id=456, toptier_agency_id=123)
    tas1 = mommy.make(
        'accounts.TreasuryAppropriationAccount',
        funding_toptier_agency=agency1_toptier)
    tas2 = mommy.make(
        'accounts.TreasuryAppropriationAccount',
        funding_toptier_agency=agency1_toptier)
    tas_bal1 = mommy.make(
        'accounts.AppropriationAccountBalances',
        final_of_fy=True,
        treasury_account_identifier=tas1,
        budget_authority_available_amount_total_cpe=1000,
        obligations_incurred_total_by_tas_cpe=2000,
        gross_outlay_amount_by_tas_cpe=3000,
        submission=sub
    )
    tas_bal2 = mommy.make(
        'accounts.AppropriationAccountBalances',
        final_of_fy=True,
        treasury_account_identifier=tas2,
        budget_authority_available_amount_total_cpe=1000,
        obligations_incurred_total_by_tas_cpe=2000.01,
        gross_outlay_amount_by_tas_cpe=-2000,
        submission=sub
    )
    # throw in some random noise to ensure only the balances for the specified
    # agency are returned in the response
    mommy.make(
        'accounts.AppropriationAccountBalances',
        _quantity=3,
        _fill_optional=True)


@pytest.mark.django_db
def test_financial_balances_agencies(client, financial_balances_models):
    """Test the financial_balances/agencies endpoint."""
    resp = client.get('/api/v2/financial_balances/agencies/?funding_agency_id=456&fiscal_year=2016')
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1
    result = resp.data['results'][0]
    assert result['budget_authority_amount'] == '2000.00'
    assert result['obligated_amount'] == '4000.01'
    assert result['outlay_amount'] == '1000.00'


@pytest.mark.django_db
def test_financial_balances_agencies_params(client, financial_balances_models):
    """Test invalid financial_balances/agencies parameters."""
    # funding_agency_id is missing
    resp = client.get('/api/v2/financial_balances/agencies/?fiscal_year=2016')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST