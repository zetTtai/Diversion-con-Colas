namespace Sensores
{
    partial class IP
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de Windows Forms

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(IP));
            this.label1 = new System.Windows.Forms.Label();
            this.ValueBeingSent = new System.Windows.Forms.NumericUpDown();
            this.label2 = new System.Windows.Forms.Label();
            this.IPValue = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.PortValue = new System.Windows.Forms.NumericUpDown();
            this.Logs = new System.Windows.Forms.Panel();
            this.Conectar = new System.Windows.Forms.Button();
            this.Desconectar = new System.Windows.Forms.Button();
            this.Temporizador = new System.Windows.Forms.Timer(this.components);
            this.label4 = new System.Windows.Forms.Label();
            this.SensorId = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.ValueBeingSent)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.PortValue)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label1.Location = new System.Drawing.Point(26, 382);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(165, 24);
            this.label1.TabIndex = 0;
            this.label1.Text = "Número enviado";
            // 
            // ValueBeingSent
            // 
            this.ValueBeingSent.Location = new System.Drawing.Point(30, 418);
            this.ValueBeingSent.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.ValueBeingSent.Name = "ValueBeingSent";
            this.ValueBeingSent.Size = new System.Drawing.Size(226, 20);
            this.ValueBeingSent.TabIndex = 2;
            this.ValueBeingSent.ValueChanged += new System.EventHandler(this.ValueBeingSent_ValueChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label2.Location = new System.Drawing.Point(26, 12);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(230, 24);
            this.label2.TabIndex = 3;
            this.label2.Text = "IP del servidor de Kafka";
            // 
            // IPValue
            // 
            this.IPValue.Location = new System.Drawing.Point(30, 39);
            this.IPValue.Name = "IPValue";
            this.IPValue.Size = new System.Drawing.Size(226, 20);
            this.IPValue.TabIndex = 4;
            this.IPValue.Text = "127.0.0.1";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label3.Location = new System.Drawing.Point(26, 72);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(157, 24);
            this.label3.TabIndex = 5;
            this.label3.Text = "Puerto de Kafka";
            // 
            // PortValue
            // 
            this.PortValue.Location = new System.Drawing.Point(30, 99);
            this.PortValue.Maximum = new decimal(new int[] {
            65555,
            0,
            0,
            0});
            this.PortValue.Name = "PortValue";
            this.PortValue.Size = new System.Drawing.Size(226, 20);
            this.PortValue.TabIndex = 6;
            this.PortValue.Value = new decimal(new int[] {
            9092,
            0,
            0,
            0});
            // 
            // Logs
            // 
            this.Logs.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Logs.AutoScroll = true;
            this.Logs.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(28)))), ((int)(((byte)(31)))), ((int)(((byte)(35)))));
            this.Logs.Location = new System.Drawing.Point(283, 12);
            this.Logs.Name = "Logs";
            this.Logs.Size = new System.Drawing.Size(725, 426);
            this.Logs.TabIndex = 7;
            // 
            // Conectar
            // 
            this.Conectar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(10)))), ((int)(((byte)(10)))), ((int)(((byte)(12)))));
            this.Conectar.FlatAppearance.BorderSize = 0;
            this.Conectar.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Conectar.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.Conectar.Location = new System.Drawing.Point(30, 260);
            this.Conectar.Name = "Conectar";
            this.Conectar.Size = new System.Drawing.Size(226, 35);
            this.Conectar.TabIndex = 8;
            this.Conectar.Text = "Conectar";
            this.Conectar.UseVisualStyleBackColor = false;
            this.Conectar.Click += new System.EventHandler(this.Conectar_Click);
            // 
            // Desconectar
            // 
            this.Desconectar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(10)))), ((int)(((byte)(10)))), ((int)(((byte)(12)))));
            this.Desconectar.Enabled = false;
            this.Desconectar.FlatAppearance.BorderSize = 0;
            this.Desconectar.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Desconectar.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.Desconectar.Location = new System.Drawing.Point(30, 310);
            this.Desconectar.Name = "Desconectar";
            this.Desconectar.Size = new System.Drawing.Size(226, 35);
            this.Desconectar.TabIndex = 9;
            this.Desconectar.Text = "Desconectar";
            this.Desconectar.UseVisualStyleBackColor = false;
            this.Desconectar.Click += new System.EventHandler(this.Desconectar_Click);
            // 
            // Temporizador
            // 
            this.Temporizador.Interval = 3000;
            this.Temporizador.Tick += new System.EventHandler(this.Temporizador_Tick);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label4.Location = new System.Drawing.Point(26, 162);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(131, 24);
            this.label4.TabIndex = 10;
            this.label4.Text = "Id del sensor";
            // 
            // SensorId
            // 
            this.SensorId.Location = new System.Drawing.Point(30, 202);
            this.SensorId.Name = "SensorId";
            this.SensorId.Size = new System.Drawing.Size(226, 20);
            this.SensorId.TabIndex = 11;
            this.SensorId.TextChanged += new System.EventHandler(this.SensorId_TextChanged);
            // 
            // IP
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(23)))), ((int)(((byte)(26)))), ((int)(((byte)(30)))));
            this.ClientSize = new System.Drawing.Size(1020, 450);
            this.Controls.Add(this.SensorId);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.Desconectar);
            this.Controls.Add(this.Conectar);
            this.Controls.Add(this.Logs);
            this.Controls.Add(this.PortValue);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.IPValue);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.ValueBeingSent);
            this.Controls.Add(this.label1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.Name = "IP";
            this.Text = "FWQ_Sensor";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.ValueBeingSent)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.PortValue)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown ValueBeingSent;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox IPValue;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown PortValue;
        private System.Windows.Forms.Panel Logs;
        private System.Windows.Forms.Button Conectar;
        private System.Windows.Forms.Button Desconectar;
        private System.Windows.Forms.Timer Temporizador;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox SensorId;
    }
}

