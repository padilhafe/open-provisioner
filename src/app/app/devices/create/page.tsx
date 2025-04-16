// app/devices/create/page.tsx

'use client';

import { useState } from 'react';

export default function DeviceFormPage() {
  const [formData, setFormData] = useState({
    hostname: '',
    device_type: '',
    device_mgmt_ipv4: '',
    device_username: '',
    device_password: '',
    device_mgmt_port: 22,
    snmp_version: 1,
    snmp_port: 161,
    snmp_community: ''
  });

  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('port') || name.includes('version') ? Number(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(false);
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/devices/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Erro ao cadastrar dispositivo.');
      }

      setSuccess(true);
      setFormData({
        hostname: '',
        device_type: '',
        device_mgmt_ipv4: '',
        device_username: '',
        device_password: '',
        device_mgmt_port: 22,
        snmp_version: 1,
        snmp_port: 161,
        snmp_community: ''
      });
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Cadastrar Novo Dispositivo</h1>

      {success && <p className="text-green-600 mb-4">Dispositivo cadastrado com sucesso!</p>}
      {error && <p className="text-red-600 mb-4">{error}</p>}

      <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
        <input className="input" name="hostname" placeholder="Hostname" value={formData.hostname} onChange={handleChange} required />
        <input className="input" name="device_type" placeholder="Tipo de Dispositivo (Ex: huawei)" value={formData.device_type} onChange={handleChange} required />
        <input className="input" name="device_mgmt_ipv4" placeholder="IP de Gerência" value={formData.device_mgmt_ipv4} onChange={handleChange} required />
        <input className="input" name="device_username" placeholder="Usuário SSH" value={formData.device_username} onChange={handleChange} required />
        <input className="input" name="device_password" placeholder="Senha SSH" type="password" value={formData.device_password} onChange={handleChange} required />
        <input className="input" name="device_mgmt_port" placeholder="Porta SSH" type="number" value={formData.device_mgmt_port} onChange={handleChange} required />
        <select className="input" name="snmp_version" value={formData.snmp_version} onChange={handleChange}>
          <option value={1}>SNMP v1</option>
          <option value={2}>SNMP v2</option>
          <option value={3}>SNMP v3</option>
        </select>
        <input className="input" name="snmp_port" placeholder="Porta SNMP" type="number" value={formData.snmp_port} onChange={handleChange} required />
        <input className="input" name="snmp_community" placeholder="SNMP Community" value={formData.snmp_community} onChange={handleChange} required />

        <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded">
          Cadastrar
        </button>
      </form>

      <style jsx>{`
        .input {
          padding: 0.5rem;
          border: 1px solid #ccc;
          border-radius: 0.375rem;
        }
      `}</style>
    </div>
  );
}
