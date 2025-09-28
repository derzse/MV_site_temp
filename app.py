from flask import Flask, render_template
from utils import SEOTitleManager
from flask import jsonify

app = Flask(__name__)

# Initialize SEO manager 
seo_manager = SEOTitleManager(strategy='random')

@app.route('/')
def home():
    """Home page with dynamic SEO title"""
    dynamic_title = seo_manager.get_title()
    return render_template('index.html', page_title=dynamic_title)

@app.template_global()
def get_seo_title():
    return seo_manager.get_title()

# Optional: View SEO stats
@app.route('/admin/seo-stats')
def seo_stats():
    """Admin endpoint to monitor title performance"""
    return jsonify({
        'strategy': seo_manager.strategy,
        'title_usage': seo_manager.get_performance_stats(),
        'total_requests': seo_manager.get_total_requests(),
        'available_titles': len(seo_manager.titles)
    })
    
# Optional: Admin endpoint to change strategy
@app.route('/admin/seo-strategy/<strategy>')
def change_seo_strategy(strategy):
    """Admin endpoint to change SEO strategy"""
    try:
        seo_manager.set_strategy(strategy)
        return jsonify({'success': True, 'new_strategy': strategy})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/about')
def about():
    return render_template('about.html')  # Assumes you have an about.html template

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')  # Assumes you have a privacy.html template


if __name__ == '__main__':
    app.run(debug=True)
