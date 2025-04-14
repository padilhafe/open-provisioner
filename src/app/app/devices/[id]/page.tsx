'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

interface UsersResponse {
  device: string;
  users: string[];
}

export default function DeviceUsersPage() {
  const { id } = useParams();
  const [data, setData] = useState<UsersResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchUsers() {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/devices/${id}/get-current-users`);
        if (!res.ok) throw new Error('Erro ao buscar usuários do dispositivo');
        const json: UsersResponse = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message || 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    }

    if (id) {
      fetchUsers();
    }
  }, [id]);

  if (loading) return <p className="p-4">Carregando usuários...</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Usuários cadastrados - {data?.device}</h1>

      {data?.users.length === 0 ? (
        <p>Nenhum usuário conectado.</p>
      ) : (
        <ul className="list-disc list-inside">
          {data?.users.map((user, index) => (
            <li key={index} className="text-gray-700">{user}</li>
          ))}
        </ul>
      )}

      <div className="mt-4">
        <a href="/devices" className="text-blue-600 hover:underline">← Voltar para a lista</a>
      </div>
    </div>
  );
}
