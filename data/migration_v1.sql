-- 1. ADICIONAR NOVAS COLUNAS À TABELA DE EVENTOS
ALTER TABLE eventos_bc 
ADD COLUMN IF NOT EXISTS data_inicio DATE,
ADD COLUMN IF NOT EXISTS data_fim DATE,
ADD COLUMN IF NOT EXISTS usar_data_fim BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS horario_inicio TIME,
ADD COLUMN IF NOT EXISTS horario_fim TIME,
ADD COLUMN IF NOT EXISTS usar_horario_fim BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS endereco TEXT,
ADD COLUMN IF NOT EXISTS ao_vivo BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS link_ao_vivo TEXT;

-- 2. CRIAR BUCKET DE IMAGENS (Se não possuir o bucket 'event_images')
INSERT INTO storage.buckets (id, name, public) 
VALUES ('event_images', 'event_images', true)
ON CONFLICT (id) DO NOTHING;

-- 3. POLÍTICAS DE ACESSO AO STORAGE
-- Removemos antes de criar para evitar erro de "já existe"
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Admin Upload" ON storage.objects;
DROP POLICY IF EXISTS "Admin Delete" ON storage.objects;

CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'event_images');
CREATE POLICY "Admin Upload" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'event_images');
CREATE POLICY "Admin Delete" ON storage.objects FOR DELETE USING (bucket_id = 'event_images');

-- 4. CRIAR TABELA DE CHECK-INS REALIZADOS
CREATE TABLE IF NOT EXISTS checkins_realizados (
    id BIGSERIAL PRIMARY KEY,
    evento_id TEXT REFERENCES eventos_bc(id),
    medico_nome TEXT,
    nomeAnuncio TEXT,
    email TEXT,
    crm TEXT,
    whatsapp TEXT,
    bio TEXT,
    data_checkin TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE checkins_realizados ENABLE ROW LEVEL SECURITY;

-- Políticas de Check-in (Remover antes de criar)
DROP POLICY IF EXISTS "Enable insert for all" ON checkins_realizados;
DROP POLICY IF EXISTS "Enable select for admin" ON checkins_realizados;

CREATE POLICY "Enable insert for all" ON checkins_realizados FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for admin" ON checkins_realizados FOR SELECT USING (true);
