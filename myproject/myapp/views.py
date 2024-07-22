
from django.shortcuts import render, redirect
from django.db import connection
import csv, json
from .forms import DataImportForm


from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedData
from .forms import ImportedDataForm



def index(request):
    import_form = DataImportForm()

    if request.method == 'POST':
        if 'import_data' in request.POST:
            import_form = DataImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                file = import_form.cleaned_data.get('file')
                if file:
                    if file.name.endswith('.csv'):
                        preview_data = preview_csv_file(file)
                    elif file.name.endswith('.json'):
                        preview_data = preview_json_file(file)
                    return render(request, 'index.html', {
                        'import_form': import_form,
                        'preview_data': preview_data,
                        'columns': preview_data['columns'],
                        'show_import_preview': True
                    })
        elif 'create_table' in request.POST:
            columns = request.POST.getlist('column_name')
            types = request.POST.getlist('column_type')
            data = json.loads(request.POST.get('data'))
            create_table_with_data(columns, types, data)
            return redirect('success')
        elif 'manual_data' in request.POST:
            columns = request.POST.getlist('manual_column_name')
            types = request.POST.getlist('manual_column_type')
            data = request.POST.get('manual_data')
            create_table_with_data(columns, types, data.split('\n'))
            return redirect('success')
    
    return render(request, 'index.html', {'import_form': import_form, 'show_import_preview': False})

def preview_csv_file(file):
    reader = csv.DictReader(file.read().decode('utf-8').splitlines())
    columns = reader.fieldnames
    rows = [row for i, row in enumerate(reader) if i < 10]  
    return {'columns': columns, 'rows': rows, 'data': list(reader)}

def preview_json_file(file):
    data = json.load(file)
    columns = data[0].keys()
    rows = data[:10]  
    return {'columns': columns, 'rows': rows, 'data': data}

def create_table_and_insert_data(data):
    if isinstance(data, csv.DictReader):
        columns = data.fieldnames
        rows = list(data)
    elif isinstance(data, list) and data:
        columns = data[0].keys()
        rows = data
    else:
        return
    
    table_name = 'dynamic_table'
    create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{col} TEXT' for col in columns])});"
    
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(create_table_query)
        for row in rows:
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"
            cursor.execute(insert_query, list(row.values()))

def create_table_with_data(columns, types, data):
    table_name = 'dynamic_table'
    column_definitions = [f"{col.strip()} {typ.strip()}" for col, typ in zip(columns, types)]
    create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)});"

    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(create_table_query)
        for row in data:
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"
            cursor.execute(insert_query, row.split(','))

def success(request):
    return render(request, 'success.html')



def get_table_columns(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            """, [table_name])
        columns = cursor.fetchall()
    return [(col[0], col[1]) for col in columns]


def data_list(request):
    table_name = 'dynamic_table' 
    columns = get_table_columns(table_name)
    # col_names = [c[0] for c in columns]
    # col_type = [c[1] for c in columns]
    return render(request, 'importer/data_list.html', {'column_data': columns})

def get_top_10_rows(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
        rows = cursor.fetchall()
    return rows


def view_data(request):
    table_name = 'dynamic_table' 
    columns = get_table_columns(table_name)
    # col_names = [c[0] for c in columns]
    # col_type = [c[1] for c in columns]
    return render(request, 'importer/data_list.html', {'column_data': columns})

def data_create(request):
    if request.method == 'POST':
        form = ImportedDataForm(request.POST)
        if form.is_valid():
            column_name = form.cleaned_data['column_name']
            column_type = form.cleaned_data['column_type']
            column_required = form.cleaned_data['column_required']
            
            
            table_name = 'dynamic_table'
            column_type_map = {
                'TEXT': 'TEXT',
                'INTEGER': 'INTEGER',
                'REAL': 'REAL',
                'BOOLEAN': 'BOOLEAN',
                'DATE': 'DATE',
                'TIMESTAMP': 'TIMESTAMP'
            }
            
            
            sql_command = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_map[column_type]}"
            
            
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
            
            
            return redirect('view_data')
    else:
        form = ImportedDataForm()

    return render(request, 'importer/data_form.html', {'form': form})

def data_update(request, id):
    item = get_object_or_404(ImportedData, id=id)
    if request.method == 'POST':
        form = ImportedDataForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('view_data')
    else:
        form = ImportedDataForm(instance=item)
    return render(request, 'importer/data_form.html', {'form': form})

def data_delete(request, id):
    item = get_object_or_404(ImportedData, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('view_data')
    return render(request, 'importer/data_confirm_delete.html', {'item': item})