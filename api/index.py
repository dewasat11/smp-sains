"""
Unified Serverless Function Router
Handles all API endpoints to stay under Vercel's 12 function limit
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):
    def _route_request(self):
        """Route request to appropriate handler based on path or action parameter"""
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            params = parse_qs(parsed.query)
            
            # Get action from query parameter or derive from path
            action = params.get('action', [''])[0]
            if not action:
                # Extract action from path: /api/index?... or /api/pendaftar_create
                if path.startswith('/api/'):
                    action = path.replace('/api/', '').split('?')[0]
                    if action == 'index' or action == '':
                        action = params.get('action', [''])[0]
            
            # Remove 'index' if present
            if action == 'index':
                action = ''
            
            print(f"Routing: {self.command} {path} -> action: {action}")
            
            # Route to appropriate handler
            if action == 'pendaftar_create':
                from api.handlers.pendaftar_create import handler as PendaftarCreateHandler
                PendaftarCreateHandler.do_POST(self) if self.command == 'POST' else PendaftarCreateHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_list':
                from api.handlers.pendaftar_list import handler as PendaftarListHandler
                PendaftarListHandler.do_GET(self) if self.command == 'GET' else PendaftarListHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_cek_status':
                from api.handlers.pendaftar_cek_status import handler as CekStatusHandler
                CekStatusHandler.do_GET(self) if self.command == 'GET' else CekStatusHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_status':
                from api.handlers.pendaftar_status import handler as StatusHandler
                StatusHandler.do_POST(self) if self.command == 'POST' else StatusHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_update_files':
                from api.handlers.pendaftar_update_files import handler as UpdateFilesHandler
                UpdateFilesHandler.do_POST(self) if self.command == 'POST' else UpdateFilesHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_files_list':
                from api.handlers.pendaftar_files_list import handler as FilesListHandler
                FilesListHandler.do_GET(self) if self.command == 'GET' else FilesListHandler.do_OPTIONS(self)
                
            elif action == 'pendaftar_download_zip':
                from api.handlers.pendaftar_download_zip import handler as DownloadZipHandler
                DownloadZipHandler.do_GET(self) if self.command == 'GET' else DownloadZipHandler.do_OPTIONS(self)
                
            elif action == 'export_pendaftar_csv':
                from api.handlers.export_pendaftar_csv import handler as ExportCSVHandler
                ExportCSVHandler.do_GET(self) if self.command == 'GET' else ExportCSVHandler.do_OPTIONS(self)
                
            elif action == 'upload_file':
                from api.handlers.upload_file import handler as UploadHandler
                UploadHandler.do_POST(self) if self.command == 'POST' else UploadHandler.do_OPTIONS(self)
                
            elif action == 'pembayaran_list':
                from api.handlers.pembayaran_list import handler as PembayaranListHandler
                PembayaranListHandler.do_GET(self) if self.command == 'GET' else PembayaranListHandler.do_OPTIONS(self)
                
            elif action == 'pembayaran_submit':
                from api.handlers.pembayaran_submit import handler as PembayaranSubmitHandler
                PembayaranSubmitHandler.do_POST(self) if self.command == 'POST' else PembayaranSubmitHandler.do_OPTIONS(self)
                
            elif action == 'pembayaran_verify':
                from api.handlers.pembayaran_verify import handler as PembayaranVerifyHandler
                PembayaranVerifyHandler.do_POST(self) if self.command == 'POST' else PembayaranVerifyHandler.do_OPTIONS(self)
                
            elif action == 'supa_proxy':
                from api.handlers.supa_proxy import handler as SupaProxyHandler
                if self.command == 'POST':
                    SupaProxyHandler.do_POST(self)
                elif self.command == 'GET':
                    SupaProxyHandler.do_GET(self)
                else:
                    SupaProxyHandler.do_OPTIONS(self)
                    
            else:
                # Default response for unknown actions
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(
                    f'{{"ok": false, "error": "Unknown action: {action}"}}'.encode()
                )
                
        except Exception as e:
            print(f"Router error: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(
                f'{{"ok": false, "error": "Router error: {str(e)}"}}'.encode()
            )
    
    def do_GET(self):
        self._route_request()
    
    def do_POST(self):
        self._route_request()
    
    def do_OPTIONS(self):
        self._route_request()

