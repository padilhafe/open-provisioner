'use client';

import { useEffect, useState } from 'react';

type Device = {
  id: number;
  hostname: string;
  device_type: string;
  device_hostname: string;
  device_mgmt_ipv4: string;
  device_username: string;
  device_password: string;
  device_mgmt_port: number;
  snmp_version: number;
  snmp_port: number;
  snmp_community: string;
};

export default function DevicesPage() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchDevices() {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/devices/');
        if (!res.ok) throw new Error('Erro ao buscar dispositivos');
        const data = await res.json();
        setDevices(data);
      } catch (err: any) {
        setError(err.message || 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    }

    fetchDevices();
  }, []);

  if (loading) return <p className="p-4">Carregando dispositivos...</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Lista de Dispositivos</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300 rounded-md">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-4 py-2 text-left">ID</th>
              <th className="border px-4 py-2 text-left">Hostname</th>
              <th className="border px-4 py-2 text-left">Tipo</th>
              <th className="border px-4 py-2 text-left">IP de Gerência</th>
              <th className="border px-4 py-2 text-left">Usuário</th>
              <th className="border px-4 py-2 text-left">Porta SSH</th>
              <th className="border px-4 py-2 text-left">SNMP</th>
              <th className="border px-4 py-2 text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            {devices.map((device) => (
              <tr key={device.id} className="hover:bg-gray-50">
                <td className="border px-4 py-2">{device.id}</td>
                <td className="border px-4 py-2">{device.hostname}</td>
                <td className="border px-4 py-2">{device.device_type}</td>
                <td className="border px-4 py-2">{device.device_mgmt_ipv4}</td>
                <td className="border px-4 py-2">{device.device_username}</td>
                <td className="border px-4 py-2">{device.device_mgmt_port}</td>
                <td className="border px-4 py-2">
                  v{device.snmp_version} @ {device.snmp_port} ({device.snmp_community})
                </td>
                <td className="border px-4 py-2">
                  {/* Aqui você pode adicionar links de ações, ex: editar hostname */}
                  <a
                    href={`/devices/${device.id}/hostname`}
                    className="text-blue-600 hover:underline"
                  >
                    Editar hostname
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}