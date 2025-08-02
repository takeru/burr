import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import anywidget
    from traitlets import List


    ThreeESM = """
    import * as THREE from "https://esm.sh/three";
    import { OrbitControls } from "https://esm.sh/three/examples/jsm/controls/OrbitControls.js";

    // クロージャーで共有状態を作成
    export default (() => {
      // カメラ状態を保持する共有オブジェクト
      let cameraState = null;

      return {
        render({ model, el }) {
          let scene, camera, renderer, controls;
          let cubes = [];  // 現在のキューブを追跡
          let animationId = null;

          let container = document.createElement("div");
          container.style.height = "400px";
          container.style.width = "600px";
          el.appendChild(container);

          scene = new THREE.Scene();
          scene.background = new THREE.Color(0x808080);  // グレー背景

          camera = new THREE.PerspectiveCamera(
            75,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
          );

          // カメラ状態を復元または初期化
          if (cameraState) {
            camera.position.copy(cameraState.position);
            camera.rotation.copy(cameraState.rotation);
          } else {
            camera.position.set(10, 10, 10);
          }

          // レンダラーの設定（影を有効化）
          renderer = new THREE.WebGLRenderer({ 
            antialias: true,        // アンチエイリアシング
            alpha: false,           // 透明背景（trueで透明）
            preserveDrawingBuffer: false,  // スクリーンショット用
            powerPreference: "high-performance"  // GPU性能設定
          });
          renderer.setSize(container.clientWidth, container.clientHeight);
          renderer.shadowMap.enabled = true;  // 影を有効化
          renderer.shadowMap.type = THREE.PCFSoftShadowMap;  // ソフトシャドウ
          container.appendChild(renderer.domElement);

          controls = new OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.05;
          controls.screenSpacePanning = false;  // 画面平行移動を無効化
          controls.minDistance = 5;
          controls.maxDistance = 50;

          // ArcRotateCameraのような動作設定
          controls.enablePan = false;    // パン操作を無効化（カメラの移動を防ぐ）
          controls.rotateSpeed = 1.0;    // 回転速度
          controls.zoomSpeed = 1.2;      // ズーム速度

          // カメラ状態を復元または初期化
          if (cameraState && cameraState.target) {
            controls.target.copy(cameraState.target);
          } else {
            controls.target.set(0, 0, 0);
          }

          camera.lookAt(controls.target);

          // カメラ状態を保存する関数
          const saveCameraState = () => {
            cameraState = {
              position: camera.position.clone(),
              rotation: camera.rotation.clone(),
              target: controls.target.clone()
            };
          };

          // カメラが変更されたときに状態を保存
          controls.addEventListener('change', saveCameraState);

          // 座標軸ヘルパーを追加（X:赤, Y:緑, Z:青）
          const axesHelper = new THREE.AxesHelper(5);
          scene.add(axesHelper);

          // ライティングの設定
          // 1. 環境光（全体を均等に照らす）
          const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
          scene.add(ambientLight);

          // 2. 指向性ライト（太陽光のような平行光線）
          const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
          directionalLight.position.set(5, 10, 5);
          directionalLight.castShadow = true;  // 影を落とす
          
          // 影の品質設定
          directionalLight.shadow.mapSize.width = 2048;
          directionalLight.shadow.mapSize.height = 2048;
          directionalLight.shadow.camera.near = 0.5;
          directionalLight.shadow.camera.far = 50;
          directionalLight.shadow.camera.left = -20;
          directionalLight.shadow.camera.right = 20;
          directionalLight.shadow.camera.top = 20;
          directionalLight.shadow.camera.bottom = -20;
          
          scene.add(directionalLight);

          // 3. ポイントライト（電球のような点光源）
          const pointLight = new THREE.PointLight(0xffffff, 0.4);
          pointLight.position.set(-5, 5, -5);
          scene.add(pointLight);

          // 4. 床面を追加（影を受ける）
          const floorGeometry = new THREE.PlaneGeometry(30, 30);
          const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x666666,
            roughness: 0.8,
            metalness: 0.2
          });
          const floor = new THREE.Mesh(floorGeometry, floorMaterial);
          floor.rotation.x = -Math.PI / 2;  // 水平に配置
          floor.position.y = -4;
          floor.receiveShadow = true;  // 影を受ける
          scene.add(floor);

          // キューブを削除する関数
          function clearCubes() {
            cubes.forEach(cube => {
              scene.remove(cube);
              if (cube.geometry) cube.geometry.dispose();
              if (cube.material) cube.material.dispose();
            });
            cubes = [];
          }

          // キューブを描画する関数
          function draw(data) {
            clearCubes();  // 既存のキューブをクリア

            for (let i = 0; i < data.length; i++) {
              const d = data[i];
              // サイズの指定（デフォルトは1）
              const size = d.size || { x: 1, y: 1, z: 1 };
              const geometry = new THREE.BoxGeometry(size.x, size.y, size.z);
              const color = new THREE.Color(d.color);
              const opacity = d.opacity;
              
              // MeshStandardMaterialに変更（物理ベースレンダリング）
              const material = new THREE.MeshStandardMaterial({ 
                color: color,
                transparent: opacity < 1.0,
                opacity: opacity,
                roughness: 0.5,    // 粗さ（0:鏡面、1:マット）
                metalness: 0.1,    // 金属性（0:非金属、1:金属）
                emissive: color,   // 発光色
                emissiveIntensity: 0.1  // 発光強度
              });
              
              const cube = new THREE.Mesh(geometry, material);
              cube.position.set(d.position.x, d.position.y, d.position.z);
              cube.castShadow = true;     // 影を落とす
              cube.receiveShadow = true;  // 影を受ける
              scene.add(cube);
              cubes.push(cube);
            }
          }

          // 初期データを描画
          const data = model.get("data");
          draw(data);

          // データが変更されたときの処理
          model.on("change:data", () => {
            const newData = model.get("data");
            draw(newData);
          });

          // アニメーションループ
          function animate() {
            animationId = requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
          }
          animate();

          // クリーンアップ関数
          return () => {
            // カメラ状態を保存
            saveCameraState();

            // アニメーションを停止
            if (animationId) {
              cancelAnimationFrame(animationId);
            }

            // イベントリスナーを削除
            controls.removeEventListener('change', saveCameraState);

            // リソースをクリーンアップ
            clearCubes();
            controls.dispose();
            renderer.dispose();
            if (axesHelper.geometry) axesHelper.geometry.dispose();
            if (axesHelper.material) axesHelper.material.dispose();
          };
        }
      };
    })();
    """


@app.class_definition
class ThreeWidget(anywidget.AnyWidget):
    _esm = ThreeESM
    data = List().tag(sync=True)


@app.cell
def _(mo):
    a = mo.ui.slider(start=0, stop=10, step=0.1)
    a
    return (a,)


@app.cell
def _(a):
    data = [
        {"position": {"x": a.value, "y": 0, "z": 0}, "color": "red", "opacity": 1.0, "size": {"x": 2, "y": 2, "z": 2}},
        {"position": {"x": 3, "y": 0, "z": 0}, "color": "green", "opacity": 0.8, "size": {"x": 1, "y": 2, "z": 1}},
        {"position": {"x": -3, "y": 0, "z": 0}, "color": "blue", "opacity": 0.6, "size": {"x": 1.5, "y": 1.5, "z": 1.5}},
        {"position": {"x": 0, "y": 3, "z": 0}, "color": "yellow", "opacity": 1.0, "size": {"x": 1, "y": 1, "z": 3}},
        {"position": {"x": 0, "y": -3, "z": 0}, "color": "purple", "opacity": 0.9, "size": {"x": 3, "y": 0.5, "z": 1}},
        {"position": {"x": 0, "y": 0, "z": 3}, "color": "orange", "opacity": 0.7},  # サイズ指定なし（デフォルト1x1x1）
        {"position": {"x": 0, "y": 0, "z": -3}, "color": "cyan", "opacity": 1.0, "size": {"x": 0.5, "y": 0.5, "z": 0.5}},
    ]


    three_widget = ThreeWidget()
    three_widget.data = data

    [three_widget, a, a.value]
    return


@app.cell
def _(a, mo):
    mo.md(f"""{a.value}""")
    return


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
