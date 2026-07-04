from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.models import Asset, AuditLog, Mitigation, Risk


class AuditLogFilterTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.other_user = get_user_model().objects.create_user(username='other', password='secret123')

        AuditLog.objects.create(user=self.user, action_type='CREATE', entity_name='Asset', entity_id='1', action_details='Created asset')
        AuditLog.objects.create(user=self.other_user, action_type='UPDATE', entity_name='Risk', entity_id='2', action_details='Updated risk')

    def test_filter_view_returns_filtered_audit_logs(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('audit_log_filter'), {
            'user_id': self.user.id,
            'action_type': 'CREATE',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['all_auditlogs'].count(), 1)
        self.assertEqual(response.context['all_auditlogs'].first().user_id, self.user.id)
        self.assertEqual(response.context['all_auditlogs'].first().action_type, 'CREATE')

    def test_page_view_sets_default_audit_log_date_values(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('page', kwargs={'page_name': 'audit_logs'}))

        self.assertEqual(response.status_code, 200)
        earliest_log_date = AuditLog.objects.order_by('action_date').first().action_date.date().strftime('%Y-%m-%d')
        self.assertEqual(response.context['selected_date_from'], earliest_log_date)
        self.assertEqual(response.context['selected_date_to'], date.today().strftime('%Y-%m-%d'))

    def test_audit_log_filter_paginates_results_to_ten_rows(self):
        self.client.force_login(self.user)

        for index in range(11):
            AuditLog.objects.create(
                user=self.user,
                action_type='UPDATE',
                entity_name='Risk',
                entity_id=str(index),
                action_details=f'Updated risk {index}',
            )

        response = self.client.get(reverse('audit_log_filter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_auditlogs']), 10)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertTrue(response.context['page_obj'].has_next())
        self.assertFalse(response.context['page_obj'].has_previous())


class ReportFilterTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='reporter', password='secret123')
        self.asset = Asset.objects.create(
            asset_name='Server A',
            asset_description='Primary server',
            asset_category='IT',
            operational_status='ACTIVE',
            classification='INTERNAL',
            asset_criticality='HIGH',
            cia_confidentiality='HIGH',
            cia_integrity='HIGH',
            cia_availability='HIGH',
            asset_owner='Owner',
            location='HQ',
        )
        self.risk = Risk.objects.create(
            asset=self.asset,
            risk_description='Risk one',
            likelihood=3,
            impact=4,
            risk_treatment='MODIFY',
            review_date='2026-07-01',
            risk_status='OPEN',
        )
        self.mitigation = Mitigation.objects.create(
            risk=self.risk,
            action_description='Patch server',
            assigned_to=self.user,
            target_date='2026-07-03',
            progress_status='NOT STARTED',
            comments='Need patch',
            effectiveness_review_date='2026-07-04',
        )

    def test_report_filter_returns_filtered_mitigation_rows(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('report_filter'), {
            'category': 'IT',
            'risk_status': 'OPEN',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['report_data']), 1)
        self.assertEqual(response.context['report_data'][0]['asset'], 'Server A')
        self.assertEqual(response.context['report_data'][0]['status'], 'OPEN')

    def test_view_risk_renders_annex_controls_as_list_items(self):
        self.client.force_login(self.user)
        self.risk.annex_control = 'Control A\nControl B'
        self.risk.save()

        response = self.client.get(reverse('view_risk', kwargs={'risk_id': self.risk.risk_id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['annex_controls'], ['Control A', 'Control B'])

    def test_report_filter_uses_default_date_values_when_none_are_provided(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('report_filter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_date_from'], self.asset.created_at.date().strftime('%Y-%m-%d'))
        self.assertEqual(response.context['selected_date_to'], date.today().strftime('%Y-%m-%d'))

    def test_report_filter_paginates_results_to_ten_rows(self):
        self.client.force_login(self.user)

        for index in range(11):
            asset = Asset.objects.create(
                asset_name=f'Server {index}',
                asset_description='Secondary server',
                asset_category='IT',
                operational_status='ACTIVE',
                classification='INTERNAL',
                asset_criticality='HIGH',
                cia_confidentiality='HIGH',
                cia_integrity='HIGH',
                cia_availability='HIGH',
                asset_owner='Owner',
                location='HQ',
            )
            risk = Risk.objects.create(
                asset=asset,
                risk_description=f'Risk {index}',
                likelihood=3,
                impact=4,
                risk_treatment='MODIFY',
                review_date='2026-07-01',
                risk_status='OPEN',
            )
            Mitigation.objects.create(
                risk=risk,
                action_description='Patch server',
                assigned_to=self.user,
                target_date='2026-07-03',
                progress_status='NOT STARTED',
                comments='Need patch',
                effectiveness_review_date='2026-07-04',
            )

        response = self.client.get(reverse('report_filter'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['report_data']), 10)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertTrue(response.context['page_obj'].has_next())
        self.assertFalse(response.context['page_obj'].has_previous())

    def test_assets_page_paginates_results_to_ten_rows(self):
        self.client.force_login(self.user)

        for index in range(11):
            Asset.objects.create(
                asset_name=f'Asset {index}',
                asset_description='Asset for pagination test',
                asset_category='IT',
                operational_status='ACTIVE',
                classification='INTERNAL',
                asset_criticality='HIGH',
                cia_confidentiality='HIGH',
                cia_integrity='HIGH',
                cia_availability='HIGH',
                asset_owner='Owner',
                location='HQ',
            )

        response = self.client.get(reverse('page', kwargs={'page_name': 'assets'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['assets']), 10)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertTrue(response.context['page_obj'].has_next())
        self.assertFalse(response.context['page_obj'].has_previous())

    def test_reports_page_paginates_results_to_ten_rows(self):
        self.client.force_login(self.user)

        for index in range(6):
            asset = Asset.objects.create(
                asset_name=f'Reports Server {index}',
                asset_description='Secondary server',
                asset_category='IT',
                operational_status='ACTIVE',
                classification='INTERNAL',
                asset_criticality='HIGH',
                cia_confidentiality='HIGH',
                cia_integrity='HIGH',
                cia_availability='HIGH',
                asset_owner='Owner',
                location='HQ',
            )
            risk = Risk.objects.create(
                asset=asset,
                risk_description=f'Reports Risk {index}',
                likelihood=3,
                impact=4,
                risk_treatment='MODIFY',
                review_date='2026-07-01',
                risk_status='OPEN',
            )
            Mitigation.objects.create(
                risk=risk,
                action_description='Patch server',
                assigned_to=self.user,
                target_date='2026-07-03',
                progress_status='NOT STARTED',
                comments='Need patch',
                effectiveness_review_date='2026-07-04',
            )

        response = self.client.get(reverse('page', kwargs={'page_name': 'reports'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['report_data']), 7)
        self.assertEqual(response.context['page_obj'].number, 1)
        self.assertFalse(response.context['page_obj'].has_next())

    def test_excel_export_returns_csv_attachment(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('report_export', kwargs={'file_format': 'excel'}), {
            'category': 'IT',
            'risk_status': 'OPEN',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="risk_report.csv"', response['Content-Disposition'])
        self.assertIn('Server A', response.content.decode())

    def test_pdf_export_returns_pdf_response(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('report_export', kwargs={'file_format': 'pdf'}), {
            'category': 'IT',
            'risk_status': 'OPEN',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="risk_report.pdf"', response['Content-Disposition'])
