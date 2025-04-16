'use client';

import { useState, useEffect } from 'react';
import DeviceFormPage from './create/page';
import DeviceUsersPage from './[id]/page';
import Navbar from '@/components/NavBar';

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
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showUsersModal, setShowUsersModal] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  useEffect(() => {
    async function fetchDevices() {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/v1/devices/?page=1&limit=10');
        if (!res.ok) throw new Error('Erro ao buscar dispositivos');
        const data = await res.json();
        setDevices(data.devices || []);
      } catch (err: any) {
        setError(err.message || 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    }

    fetchDevices();
  }, []);

  const handleDetailsClick = (device: Device) => {
    setSelectedDevice(device);
    setShowDetailsModal(true);
  };

  const handleUsersClick = (device: Device) => {
    setSelectedDevice(device);
    setShowUsersModal(true);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      {/* Conteúdo principal */}
      <main className="p-6">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold">Lista de Dispositivos</h1>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Criar Dispositivo
            </button>
          </div>

          {loading && <p>Carregando dispositivos...</p>}
          {error && <p className="text-red-600">{error}</p>}

          {!loading && !error && (
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-gray-300 rounded-md">
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
                        v{device.snmp_version} @ {device.snmp_port}<br />
                        ({device.snmp_community})
                      </td>
                      <td className="border px-4 py-2 space-x-2">
                        <button
                          onClick={() => handleDetailsClick(device)}
                          className="text-blue-600 hover:underline"
                        >
                          Detalhes
                        </button>
                        <button
                          onClick={() => handleUsersClick(device)}
                          className="bg-blue-600 text-white px-2 py-1 rounded-md hover:bg-blue-700"
                        >
                          Usuários
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>

      {/* Modal de criação de dispositivo */}
      {showCreateModal && (
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center z-50"
          onClick={() => setShowCreateModal(false)}
        >
          <div
            className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowCreateModal(false)}
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
            >
              X
            </button>
            <DeviceFormPage />
          </div>
        </div>
      )}

      {/* Modal de visualição de usuários */}
      {showUsersModal && selectedDevice && (
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center z-50"
          onClick={() => setShowUsersModal(false)}
        >
          <div
            className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowUsersModal(false)}
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
            >
              X
            </button>
            <DeviceUsersPage id={selectedDevice.id} />
          </div>
        </div>
      )}

      {/* Modal de detalhes do dispositivo */}
      {showDetailsModal && selectedDevice && (
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center z-50"
          onClick={() => setShowDetailsModal(false)}
        >
          <div
            className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowDetailsModal(false)}
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
            >
              X
            </button>

            <h2 className="text-xl font-bold mb-4">Detalhes do Dispositivo</h2>
            <p><strong>ID:</strong> {selectedDevice.id}</p>
            <p><strong>Hostname:</strong> {selectedDevice.hostname}</p>
            <p><strong>Tipo:</strong> {selectedDevice.device_type}</p>
            <p><strong>Hostname do Equipamento:</strong> {selectedDevice.device_hostname}</p>
            <p><strong>IP de Gerência:</strong> {selectedDevice.device_mgmt_ipv4}</p>
            <p><strong>Usuário:</strong> {selectedDevice.device_username}</p>
            <p><strong>Porta SSH:</strong> {selectedDevice.device_mgmt_port}</p>
            <p><strong>SNMP:</strong> v{selectedDevice.snmp_version} @ {selectedDevice.snmp_port}</p>
            <p><strong>Comunidade SNMP:</strong> {selectedDevice.snmp_community}</p>
          </div>
        </div>
      )}
    </div>
  );
}