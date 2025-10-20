from http.server import BaseHTTPRequestHandler
import json
from ._supabase import supabase_client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get all pembayaran from pembayaran table, ordered by newest first
            supa = supabase_client(service_role=True)
            result = supa.table('pembayaran').select("*").order('created_at', desc=True).execute()

            # Get data safely
            raw_data = result.data if result else []
            # Map fields for frontend compatibility dengan field yang konsisten
            result_data = []
            for item in raw_data:
                mapped = {
                    'id': item.get('id'),
                    'nomor_pembayaran': item.get('nomor_pembayaran'),
                    'nomor_registrasi': item.get('nomor_registrasi'),
                    'nama_lengkap': item.get('nama_lengkap'),
                    'jumlah': float(item.get('jumlah', 0)),
                    'status': item.get('status_pembayaran'),  # Gunakan field yang benar
                    'tanggal_upload': item.get('tanggal_upload'),
                    'tanggal_verifikasi': item.get('tanggal_verifikasi'),
                    'verified_by': item.get('verified_by'),
                    'catatan_admin': item.get('catatan_admin'),
                    'bukti_pembayaran': item.get('bukti_pembayaran'),
                    'metode_pembayaran': item.get('metode_pembayaran'),
                    'created_at': item.get('created_at'),
                    'updated_at': item.get('updated_at')
                }
                result_data.append(mapped)

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response_data = {
                'success': True,
                'data': result_data if result_data else [],
                'count': len(result_data) if result_data else 0
            }

            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in pembayaran_list: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e),
                'data': [],
                'count': 0
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()