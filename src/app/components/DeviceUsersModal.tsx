// components/DeviceUsersModal.tsx
'use client';

import { useEffect, useState } from 'react';

type Props = {
  deviceId: number;
};

type User = {
  username: string;
};

export default function DeviceUsersModal({ deviceId }: Props) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchUsers() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/devices/${deviceId}/users`);
        if (!res.ok) throw new Error('Erro ao buscar usuários do dispositivo');
        const data = await res.json();
        setUsers(data.users || []);
      } catch (err: any) {
        setError(err.message || 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    }

    fetchUsers();
  }, [deviceId]);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Usuários do Dispositivo {deviceId}</h2>
      {loading && <p>Carregando...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && !error && (
        <ul className="list-disc pl-5">
          {users.map(user => (
            <li key={user.username}>{user.username}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
