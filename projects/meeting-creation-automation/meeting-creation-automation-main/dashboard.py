"""
Simple web dashboard for monitoring the AI Meeting Automation system.
Run with: python dashboard.py
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime, timedelta
import sqlite3
from ai_meeting_automation import EmailProcessor

app = Flask(__name__)

# Simple database for tracking statistics
def init_db():
    conn = sqlite3.connect('automation_stats.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            emails_processed INTEGER,
            meetings_created INTEGER,
            total_emails INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Meeting Automation Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #333; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .stat-card { text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #4CAF50; }
            .stat-label { color: #666; margin-top: 5px; }
            .recent-activity { margin-top: 20px; }
            .activity-item { padding: 10px; border-left: 4px solid #4CAF50; margin: 10px 0; background: #f9f9f9; }
            .status { padding: 5px 10px; border-radius: 4px; font-size: 0.9em; }
            .status.success { background: #d4edda; color: #155724; }
            .status.info { background: #d1ecf1; color: #0c5460; }
            .refresh-btn { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        </style>
        <script>
            function refreshData() {
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('total-emails').textContent = data.total_emails;
                        document.getElementById('meetings-created').textContent = data.meetings_created;
                        document.getElementById('success-rate').textContent = data.success_rate + '%';
                        document.getElementById('last-run').textContent = data.last_run;
                    });
            }
            
            function runAutomation() {
                document.getElementById('status').innerHTML = '<span class="status info">Running automation...</span>';
                fetch('/api/run')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('status').innerHTML = '<span class="status success">Automation completed successfully</span>';
                            refreshData();
                        } else {
                            document.getElementById('status').innerHTML = '<span class="status error">Error: ' + data.error + '</span>';
                        }
                    });
            }
            
            setInterval(refreshData, 30000); // Refresh every 30 seconds
        </script>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="header">🤖 AI Meeting Automation Dashboard</h1>
                <p style="text-align: center; color: #666;">Monitor your intelligent email-to-meeting automation</p>
            </div>
            
            <div class="stats">
                <div class="card stat-card">
                    <div class="stat-number" id="total-emails">0</div>
                    <div class="stat-label">Emails Processed</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-number" id="meetings-created">0</div>
                    <div class="stat-label">Meetings Created</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-number" id="success-rate">0</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="card stat-card">
                    <div class="stat-number" id="last-run">Never</div>
                    <div class="stat-label">Last Run</div>
                </div>
            </div>
            
            <div class="card">
                <h3>Quick Actions</h3>
                <button class="refresh-btn" onclick="runAutomation()">🚀 Run Automation Now</button>
                <button class="refresh-btn" onclick="refreshData()" style="background: #2196F3; margin-left: 10px;">🔄 Refresh Data</button>
                <div id="status" style="margin-top: 10px;"></div>
            </div>
            
            <div class="card recent-activity">
                <h3>Recent Activity</h3>
                <div id="activity-list">
                    <div class="activity-item">
                        <strong>System started</strong><br>
                        <small>Dashboard initialized and ready for monitoring</small>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Initial data load
            refreshData();
        </script>
    </body>
    </html>
    '''

@app.route('/api/stats')
def get_stats():
    """Get automation statistics."""
    try:
        conn = sqlite3.connect('automation_stats.db')
        c = conn.cursor()
        
        # Get total stats
        c.execute('SELECT SUM(emails_processed), SUM(meetings_created), SUM(total_emails) FROM email_stats')
        totals = c.fetchone()
        
        # Get last run time
        c.execute('SELECT timestamp FROM email_stats ORDER BY timestamp DESC LIMIT 1')
        last_run = c.fetchone()
        
        conn.close()
        
        total_emails = totals[2] or 0
        meetings_created = totals[1] or 0
        success_rate = round((meetings_created / total_emails * 100) if total_emails > 0 else 0, 1)
        
        return jsonify({
            'total_emails': total_emails,
            'meetings_created': meetings_created,
            'success_rate': success_rate,
            'last_run': last_run[0] if last_run else 'Never'
        })
        
    except Exception as e:
        return jsonify({
            'total_emails': 0,
            'meetings_created': 0,
            'success_rate': 0,
            'last_run': 'Error',
            'error': str(e)
        })

@app.route('/api/run')
def run_automation():
    """Manually trigger the automation."""
    try:
        processor = EmailProcessor()
        results = processor.process_emails()
        
        # Save stats
        emails_processed = len(results)
        meetings_created = sum(1 for r in results if r.get('meeting_created'))
        
        conn = sqlite3.connect('automation_stats.db')
        c = conn.cursor()
        c.execute('INSERT INTO email_stats (emails_processed, meetings_created, total_emails) VALUES (?, ?, ?)',
                  (emails_processed, meetings_created, emails_processed))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'emails_processed': emails_processed,
            'meetings_created': meetings_created,
            'results': results[:5]  # Return first 5 results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    init_db()
    print("🚀 Starting AI Meeting Automation Dashboard...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔧 n8n Interface: http://localhost:5678")
    app.run(host='0.0.0.0', port=5000, debug=True)
