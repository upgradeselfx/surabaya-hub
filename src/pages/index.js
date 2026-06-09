import { createClient } from '@supabase/supabase-js';

// Ganti dengan URL dan KEY Supabase milikmu
const supabase = createClient('URL_SUPABASE_MU', 'KEY_SUPABASE_MU');

export async function getServerSideProps() {
  const { data } = await supabase.from('listings').select('*').order('created_at', { ascending: false });
  return { props: { listings: data } };
}

export default function Home({ listings }) {
  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Lowongan Kerja Surabaya Terbaru</h1>
      {listings.map((item) => (
        <div key={item.id} style={{ borderBottom: '1px solid #ccc', padding: '10px 0' }}>
          <h3>{item.title}</h3>
          <a href={item.url} target="_blank">Lihat Detail</a>
        </div>
      ))}
    </div>
  );
}
